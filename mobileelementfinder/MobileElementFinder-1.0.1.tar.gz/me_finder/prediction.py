"""Functions for finding and validating MGEs. """
import logging
import math
from configparser import ConfigParser
from itertools import groupby
from typing import Dict, Iterator, List, Optional, Tuple, Union

import attr
from mypy_extensions import TypedDict

from mgedb import MGEdb, Sequence, Sequences
from mgedb.db import MgeType

from .context import ExecutionContext
from .errors import CoordOutOfBoundsError
from .io import ContigSequences
from .result import Alignment, MgeFinderResult, MgeResult, PredictionEvidence, TemplateSequence
from .tools import BlastHit, BlastHsp, iter_blast_hits

LOG = logging.getLogger(__name__)

# Type declaration
HSP_BIN = Tuple[BlastHsp, ...]
HSP_BINS = Tuple[HSP_BIN, ...]
ELEM_COORD = Tuple[int, int]
ALIGNMENTS = Tuple[Alignment, ...]


@attr.s(auto_attribs=True, frozen=True, slots=True)
class ElementHit:
    """Blast hit."""

    query_name: str
    query_length: int
    subject_name: str
    tot_aln_cov: float
    avg_seq_id: float
    n_gaps: int
    n_subs: int
    element_len: int
    subject_len: int
    depth: Optional[float]
    e_value: float
    cigar: str
    hsps: Tuple[BlastHsp, ...]


def _is_valid_hit(hit: ElementHit, cfg: ConfigParser) -> bool:
    """Validate good hits."""
    if hit.tot_aln_cov < cfg.getfloat('validation', 'coverage'):
        return False

    # combined hsp len is larger than reference seqeunce
    if (hit.subject_len * 1.05) < hit.element_len:
        return False

    # if no hit is significant
    if not any(h.e_value == 0 for h in hit.hsps):
        evals = (math.log10(h.e_value) for h in hit.hsps)
        if max(evals) > cfg.getfloat('validation', 'e_value'):
            return False
            
    # if hit.avg_seq_id < cfg.getfloat('validation', 'identity'):
    #     return False

    return True


def _calc_tot_aln_cov(group: HSP_BIN, hit: BlastHit) -> Union[int, float]:
    """Calculate total alignement coverage of group of hsps."""
    tot_len = sum(_hsp_len(hsp) for hsp in group)
    num_gaps = sum(int(hsp.num_gaps) for hsp in group)
    subject_len = int(hit.subject_len)
    return (tot_len - num_gaps) / subject_len


def _avg_seq_ident(group: HSP_BIN, hit: BlastHit) -> float:
    """Calculate total alignement coverage of group of hsps."""
    ident_nt = sum(float(hsp.identity) * _hsp_len(hsp) for hsp in group)
    return ident_nt / sum(_hsp_len(hsp) for hsp in group)


def _hsp_len(hsp: BlastHsp) -> int:
    """Get hsp length."""
    r_start, r_end = sorted([hsp.query_end, hsp.query_start])
    return r_end - r_start + 1


def _get_elem_coord(mge_hit: ElementHit) -> ELEM_COORD:
    """Get start and end coordinates from hit."""
    start = min(mge_hit.hsps, key=lambda x: x.query_start).query_start
    end = max(mge_hit.hsps, key=lambda x: x.query_end).query_end
    return start, end


def _get_possible_elem_coord(hsps: List[BlastHsp],
                             subject_length: int,
                             padding=1) -> Tuple[int, int]:
    """Get the possible start, end positions for given element.

    Possible positions while still containing given HSPs.
    Extra flexibility can be given by assigning the percentage of padding
    to be added to each coordinate.
    """
    seg_start = min(hsps, key=lambda x: x.query_start).query_start
    seg_end = max(hsps, key=lambda x: x.query_end).query_end
    hsps_len = seg_end - seg_start
    if hsps_len > subject_length:
        # sanity check
        raise CoordOutOfBoundsError(
            f'sum(HSPs len): {hsps_len} > subject len: {subject_length}')

    exp_start = int(seg_end - (subject_length * padding))
    return (
        exp_start if exp_start > 0 else 0,  # cant be less than 0
        int(seg_start + (subject_length * padding)))


def _group_hsps(hit: BlastHit) -> HSP_BINS:
    """Group HSPs that are likely part of same MGE.

    HSP considered part of mge if its wihtin len(template mge) - len(ref hsp)
    from reference hsp.

    Eg 1
    ref mge:    >--------------<
    ref mge:            >--------------<
    ref hsp:            |xxxxxx|

    Eg 2
    ref mge:   >--------------<
    ref mge:      >--------------<
    ref hsp:      |xxxxxx| |xx|
    """

    hsps = [h for h in hit.hsps]
    ref_hsp_idx = hsps.index(max(hsps, key=_hsp_len))
    bins = [[hsps.pop(ref_hsp_idx)]]
    # TODO add evalue validation of hsps
    for _ in range(len(hsps)):
        hsp = hsps.pop()
        h_elem = (hsp.query_start, hsp.query_end)
        has_been_added = False
        # try adding hsp to existing bins
        for curr_bin in bins:
            if any(
                    _is_contained(h_elem, (b.query_start, b.query_end))
                    for b in curr_bin):
                has_been_added = True
                break

            try:
                bin_elem = _get_possible_elem_coord(curr_bin,
                                                    hit.subject_len,
                                                    padding=1.1)
            except CoordOutOfBoundsError as err:
                LOG.debug('%s, skipping bin' % err.args[0])
                continue

            if _is_contained(h_elem, bin_elem) and not has_been_added:
                # if overlapping with putative mge length
                curr_bin.append(hsp)
                has_been_added = True

        if not has_been_added:
            # add to new bin
            bins.append([hsp])

    # TODO check for overlaping subject sequences
    return tuple(tuple(g) for g in bins)  # to imutable


def _bin_hits(hits: Iterator[ElementHit]):
    """Bin hits based on their corrdinates.

    First hit is considered as representative of a bin.
    Other hits are binned if it is contained in representative,
    If their start or end is within DISTANCE % distance from ref start and end.
    """
    bins = [[next(hits)]]
    for hit in hits:
        elem_coord = _get_elem_coord(hit)
        bin_idx = None
        for idx, curr_bin in enumerate(bins):
            reprs = curr_bin[0]  # get element representative for group
            # Get approximate start and end positions
            padded_pos = _pad_mge_coord(reprs, 0)
            if _is_overlapping(elem_coord, padded_pos):
                bin_idx = idx
                break
        if bin_idx is not None:
            bins[bin_idx].append(hit)
        else:
            bins.append([hit])
        bin_idx = None
    return bins


def _is_contained(first: ELEM_COORD, second: ELEM_COORD) -> bool:
    """Is first element nested in second element.

    Each element consists of a list with paired start, end values.
    """
    f_start, f_end = first
    s_start, s_end = second
    return s_start <= f_start and f_end <= s_end


def _is_overlapping(first: ELEM_COORD,
                    second: ELEM_COORD,
                    allowed_overlap: int = 5) -> bool:
    """Check if first gene is overlapping second."""
    if allowed_overlap < 0:
        raise ValueError('Allowed overlap must be > 0')
    # if nested, call as overlapping
    if _is_contained(first, second):
        return True
    # check overlap
    frange = set(range(first[0], first[1]))
    srange = set(range(second[0], second[1]))
    return allowed_overlap < len(frange & srange)


def _pad_mge_coord(elem: ElementHit, padding: float) -> Tuple[int, int]:
    """Get range around element padded with X%."""
    start, end = _get_elem_coord(elem)
    length = (end - start) * padding
    nstart = start - (length / 2) if start - (length / 2) >= 0 else 0
    return round(nstart), round(end + (length / 2))


def _get_mge_hit(blast_hit: ElementHit) -> Dict[str, str]:
    """Parse MGE name, allele no and accession number from blast hit."""
    name, allele, accnr = blast_hit.subject_name.split('|')
    return {'name': name, 'seq_no': allele, 'accession': accnr}


def _join_cigar(hsps: HSP_BIN) -> str:
    """Join hsp alignment cigar strings.

    Unaligned regions are denoted with N.
    """
    # get first hsp
    prev, *rest = sorted(hsps, key=lambda x: x.query_start)
    cigar = prev.cigar
    t = []
    for h in rest:
        dist_between_hsp = h.query_start - prev.query_end - 1
        t.append(dist_between_hsp)
        cigar += f' N{dist_between_hsp} {h.cigar}'
        prev = h  # store current hsp
    return cigar


def _identify_mges(ctx: ExecutionContext, blast_result: str,
                   contigs: ContigSequences,
                   db: MGEdb) -> Tuple[MgeFinderResult, Sequences, ALIGNMENTS]:
    """Find valid mobile element from blast reult and annotate output.

    HSPs for each hit is combined and the total alignment is summarized. The quality of the total
    alignment is evaluated were only valid hits are kept.

    Returns a tuple with [prediction resultr, sequence, alignments]

    """
    cfg = ctx.config  # read config
    valid_mges = []
    for hit in iter_blast_hits(blast_result):  # type: BlastHit
        for el_hsps in _group_hsps(hit):
            # TODO find better way of combining e-value.
            # summarize hit quality metrics
            element = ElementHit(tot_aln_cov=_calc_tot_aln_cov(el_hsps, hit),
                                 avg_seq_id=_avg_seq_ident(el_hsps, hit),
                                 n_gaps=sum(h.num_gaps for h in el_hsps),
                                 n_subs=sum(h.num_subs for h in el_hsps),
                                 element_len=sum(_hsp_len(g) for g in el_hsps),
                                 subject_len=hit.subject_len,
                                 depth=hit.depth,
                                 query_name=hit.query_name,
                                 query_length=hit.query_len,
                                 subject_name=hit.subject_name,
                                 e_value=min(h.e_value for h in el_hsps),
                                 cigar=_join_cigar(el_hsps),
                                 hsps=el_hsps)

            if _is_valid_hit(element, cfg):
                valid_mges.append(element)

    mge_records = db.records  # read records to memeory

    mge_sequences: List[Sequence] = []
    mge_headers = []  # store fasta headers of selected seqs
    mges = []
    alignments = []
    mge_indexer = 1
    for _, hits in groupby(valid_mges, key=lambda x: x.query_name):
        for hit_bin in _bin_hits(hits):
            best_hit = max(hit_bin,
                           key=lambda h:
                           (h.tot_aln_cov, h.avg_seq_id, h.subject_len))
            header_info = _get_mge_hit(best_hit)
            entry = mge_records[header_info['name']]

            start, end = _get_elem_coord(best_hit)
            mge_seq = contigs.sub_sequence(start - 1, end, 1,
                                           best_hit.query_name)

            # store fasta header
            header = '|'.join([
                header_info['name'], header_info['seq_no'],
                header_info['accession']
            ])
            mge_headers.append(header)
            # add header to sequence
            mge_seq = attr.evolve(mge_seq, title=header)

            # Prevent that duplicated sequences are added
            # TODO clean up
            if mge_seq in mge_sequences:
                # store id of previously stored sequence
                mge_id = int(mge_sequences[mge_seq].title.split('|')[1])
            else:
                header = f'{header_info["name"]}|{mge_indexer}'
                mge_id = mge_indexer
                # if header in (s.title for s in mge_sequences):
                #     pass
                mge_sequences.append(Sequence(title=header,
                                                  seq=mge_seq.seq))
            template = entry.sequences[int(header_info['seq_no']) - 1]

            template = TemplateSequence(accession=template.accession,
                                        start=template.start,
                                        end=template.end)
            # make entry
            mges.append(
                MgeResult(
                    mge_id=str(mge_id),
                    name=entry.name,
                    synonyms=entry.synonyms,
                    family=entry.family,
                    group=entry.group,
                    type=entry.type,
                    reference_link=entry.link,
                    evidence=PredictionEvidence.PREDICTED,
                    template=template,
                    reference=entry.references,
                    alias=entry.synonyms,
                    seq_no=int(header_info['seq_no']),
                    start=start,
                    end=end,
                    strand=best_hit.hsps[0].hit_strand,
                    contig=best_hit.query_name,
                    contig_length=best_hit.query_length,
                    identity=best_hit.avg_seq_id,
                    coverage=best_hit.tot_aln_cov,
                    depth=best_hit.depth,
                    e_value=best_hit.e_value,
                    gaps=best_hit.n_gaps,
                    substitutions=best_hit.n_subs,
                    allele_seq_length=len(mge_seq),
                    template_length=best_hit.subject_len,
                    num_hsps=len(best_hit.hsps),
                    carried_motifs=[],
                    cigar=best_hit.cigar))
            for hsp_no, hsp in enumerate(best_hit.hsps, start=1):
                alignments.append(
                    Alignment(name=entry.name,
                              mge_id=str(mge_id),
                              hsp_no=hsp_no,
                              subject_start=hsp.subject_start,
                              subject_end=hsp.subject_end,
                              query_seq=hsp.query_seq,
                              midline=hsp.midline,
                              subject_seq=hsp.subject_seq))
            mge_indexer += 1
    # TODO simplify this function
    return tuple(mges), tuple(mge_sequences), tuple(alignments)


def compose_cn_mge_id(mge_cnt, first_is, second_is):
    """Build mge_id for composite transposons."""
    return f'{mge_cnt}_{first_is.mge_id}_{second_is.mge_id}'


def _infer_putative_composite_tn(
        ctx: ExecutionContext,
        mges: MgeFinderResult,
        contigs: ContigSequences,
) -> Tuple[MgeFinderResult, Sequences]:
    """Infer putative composite transposons from prediction result.

    Composite transposon is defined by two insertion sequences that are less than
    THRESHOLD - len(insertion sequence) nucleotide aparat. The threshold is defined in the config file.

    List of MgeRecords file.
    """
    cfg = ctx.config
    RawEntry = TypedDict(
        'RawEntry', {
            'mge_id': int,
            'length': int,
            '5p_flank': MgeResult,
            '3p_flank': MgeResult,
            'contig': str,
            'sequence': None
        })
    raw_ctn: Dict[str, RawEntry] = {}
    # find potential composite transposon
    for contig, vals in groupby(mges, key=lambda x: x.contig):
        for _, identical_mges in groupby(vals, key=lambda x: x.name):
            gr_mges: List[MgeResult] = list(identical_mges)  # allow for repeated iteration
            mge_id = int(max(gr_mges, key=lambda x: int(x.mge_id)).mge_id) + 1
            ins_seq = sorted(
                [mge for mge in gr_mges if mge.type == MgeType.INSERTION_SEQUENCE],
                key=lambda x: x.start)
            if len(ins_seq) > 1:
                # check length for each insertion sequence pair
                for i in range(len(ins_seq) - 1):
                    first_is, second_is = ins_seq[
                        i:i + 2]  # type: Tuple[MgeResult, MgeResult]
                    segment_len = second_is.end - first_is.start + 1
                    if segment_len < cfg.getint('composite_transposon', 'max_len'):
                        # composite transposon
                        raw_ctn[contig] = {
                            'mge_id': compose_cn_mge_id(mge_id, first_is,
                                                        second_is),
                            'length': segment_len,
                            '5p_flank': first_is,
                            '3p_flank': second_is,
                            'contig': contig,
                            'sequence': None
                        }
                        mge_id += 1

    putative_ctn = []
    ctn_sequences = set()
    # annotate with sequence and create MgeMges object
    if raw_ctn:
        for fa in contigs:  # type: Sequence
            contig_name: str = fa.title
            entry = raw_ctn.get(contig_name)
            if entry:
                start: int = entry['5p_flank'].start - 1
                end: int = entry['3p_flank'].end
                sequence = fa.seq[start:end]
                entry['sequence'] = sequence  # get sequence from contig
                assert len(sequence) == entry['length']

                mge_id = entry['mge_id']
                cn_name = f'cn_{entry["length"]}_{entry["5p_flank"].name}'
                header = f'{cn_name}|{mge_id}'
                ctn_sequences.add(Sequence(title=header, seq=sequence))
                # make new mge entry with putative composite transposon
                putative_ctn.append(
                    attr.evolve(entry['5p_flank'],
                                mge_id=mge_id,
                                name=cn_name,
                                synonyms=[],
                                type=MgeType.COMPOSITE_TRANSPOSON,
                                evidence=PredictionEvidence.PUTATIVE,
                                reference=[],
                                alias=[],
                                start=entry['5p_flank'].start,
                                end=entry['3p_flank'].end,
                                allele_seq_length=entry['length'],
                                template_length=None,
                                carried_motifs=[],
                                cigar=None))
    return tuple(putative_ctn), tuple(ctn_sequences)


def predict_mges(ctx: ExecutionContext, blast_result: str,
                 contigs: ContigSequences,
                 db: MGEdb) -> Tuple[MgeFinderResult, Sequences, ALIGNMENTS]:
    """Predict mges with annotated sequence depth."""
    mges, mge_sequences, alignments = _identify_mges(
        ctx, blast_result, contigs,
        db)  # type: (MgeFinderResult, Sequences, ALIGNMENTS)
    put_ctn, ctn_sequences = _infer_putative_composite_tn(
        ctx, mges, contigs)  # type: (MgeFinderResult, Sequences)
    return mges + put_ctn, mge_sequences + ctn_sequences, alignments
