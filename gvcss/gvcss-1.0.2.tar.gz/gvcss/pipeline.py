from gvc4fastq import bwa_samtools
from gvc4bam import license_job
from gvc4bam import gvc_vcf_pipeline as bam_vcf_pipeline
from .gvc_variant_pipeline import gvcss_variant_pipeline
from runner.job import JobFactory
from toil.common import Toil
from toil.job import Job
import argparse
import os
import json
from collections import OrderedDict
import logging
import sys
import copy
import multiprocessing

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("pipeline")


def pipeline( max_cores, input_data, bed, dbsnp, gvc_lib, reference,
             outpath):
    
    version_filename = gvc_lib + '/version.json'
    with open(version_filename) as F:
        version = json.load(F, object_pairs_hook=OrderedDict)


    all_reads = get_tumor_all_reads(input_data)
    if bed:
        volumes = bam_vcf_pipeline.get_dynamic_volumes(bed, dbsnp, gvc_lib,
                                                       reference, outpath, *all_reads)
    else:
        volumes = bam_vcf_pipeline.get_dynamic_volumes(dbsnp, gvc_lib,
                                                       reference, outpath, *all_reads)

    check_volumes = copy.deepcopy(volumes)
    check_volumes[gvc_lib] = {"bind": "/Genowis", "mode": "rw"}
    start_job = Job()

    sample_name, paired_reads = ("T", input_data['T'])
    tumor_bam = bwa_samtools.mapping_pipeline(
        start_job, ','.join(paired_reads['R1']), ','.join(paired_reads['R2']),
        reference, outpath, sample_name, version, check_volumes, max_cores)

    start_job = gvcss_variant_pipeline(start_job, gvc_lib, reference, dbsnp,
                                       bed, outpath, [tumor_bam], 1000000,
                                       sample_name, version, volumes,
                                       check_volumes)

    return start_job


def check_single_fastq(inputjson):
    with open(inputjson) as F:
        readsdict = json.load(F, object_pairs_hook=OrderedDict)

    if len(readsdict) != 1 or 'T' not in readsdict:
        logger.error('input json format error')
        sys.exit(-1)

    for bam in readsdict['T']['R1']:
        if not os.path.exists(bam):
            logger.error('{} not exist'.format(bam))
            sys.exit(-2)

    for bam in readsdict['T']['R2']:
        if not os.path.exists(bam):
            logger.error('{} not exist'.format(bam))
            sys.exit(-3)
    return readsdict


def get_tumor_all_reads(reads):
    all_reads = list()
    all_reads += reads['T']['R1']
    all_reads += reads['T']['R2']
    return all_reads


def toil_pipeline_run(pipeline_options):
    options = Job.Runner.getDefaultOptions(
        os.path.join(pipeline_options.outpath, "jobstore"))
    options.clean = 'always'
    reads = check_single_fastq(pipeline_options.input_json)
    absPath = os.path.abspath(os.path.dirname(__file__))
   # version_filename = os.path.join(absPath, '..', 'version.json')
#    version_filename = pipeline_options.gvc_lib + '/version.json'
#    with open(version_filename) as F:
#        version_json = json.load(F, object_pairs_hook=OrderedDict)

    max_cores = int(pipeline_options.maxCores
                    ) if options.maxCores else multiprocessing.cpu_count()

    with Toil(options) as toil:
        if not toil.options.restart:
            toil.start(
                pipeline( max_cores, reads, pipeline_options.bed,
                         pipeline_options.dbsnp, pipeline_options.gvc_lib,
                         pipeline_options.reference, pipeline_options.outpath))
        else:
            toil.restart()
