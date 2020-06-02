import argparse

from gvcss.pipeline import toil_pipeline_run


def cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_json',
        help=
        'The json file stores names and paths of both normal and tumor samples.'
        + '\n' +
        'eg: { "T": { "R1": ["/disk/N_R1_1.fastq.gz", "/disk/N_R1_2.fastq.gz"],'
        '"R2":["/disk/N_R2_1.fastq.gz","/disk/N_R2_2.fastq.gz"]}'
        '}')
    parser.add_argument('reference', help='The reference fasta file')
    parser.add_argument('outpath', help='The output folder')
    parser.add_argument(
        '--dbsnp',
        help="The Single Nucleotide Polymorphism Database(dbSNP) file",
        required=True)
    parser.add_argument(
        '--bed',
        help=
        """BED file for WES or Panel analysis. It should be a TAB delimited file
with at least three columns: chrName, startPosition and endPostion""")
    parser.add_argument(
        '--segmentSize',
        type=int,
        help=
        "Chromosome segment size for each GVC job, set to 100000000 (100MB) or larger for better performance. Default is to run only one GVC job."
    )
    parser.add_argument('--gvc_lib', help="GVC library folder(license dir)")
    parser.add_argument('--strategy',
                        choices=['WES', 'WGS', 'Panel'],
                        help='Switch algorithm for WES, Panel or WGS analysis')
    parser.add_argument('--sample_name',
                        help="Name of the sample to be analyzed.",
                        default='sample_name')
    parser.add_argument('--rmtmp',
                        action='store_true',
                        default=False,
                        help='remove tempelate file')
    parser.add_argument(
        '--maxMemory',
        help="The maximum amount of memory to request from the batch" + '\n' +
        "system at any one time, eg: 32G.")
    parser.add_argument(
        '--maxCores',
        help="The maximum number of CPU cores to request from the batch" +
        '\n' + "system at any one time, eg: 8.")
    return parser.parse_args()


if __name__ == "__main__":
    pipeline_options = cmd_parser()
    toil_pipeline_run(pipeline_options)
