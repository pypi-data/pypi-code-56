from gvc4bam.gvc_pipeline import gvc_pipeline
from gvc4bam.bed_check_sort_reg import bed_check_sort_reg
from gvc4bam.qc_pipeline import qc_pipeline
import os
import re
import logging

from toil.job import Job
from runner.runner import docker_runner, decorator_wrapt
import ssinfo_interface


class single_sample_feature2vcf(Job):

    @decorator_wrapt
    def __init__(self, filter_file, bed_file, variant ,tumor_bam , reference , sample_name , output_file , image, volumes,*args,**kwargs):
        self.image = image
        self.volumes = volumes
        self.commandLine = ['sh','/usr/bin/single_sample_feature2vcf.sh',filter_file, bed_file, variant ,tumor_bam , reference , sample_name , output_file]
        super(single_sample_feature2vcf,self).__init__(*args,**kwargs)

    @docker_runner('single_sample_feature2vcf')
    def run(self, fileStore):
        return self.commandLine


def single_sample_feature2vcf_pipeline (root,feature_dict, bed_sort_file, gvc_varians ,bam_list , reference , sample_name , outpath, version, volumes ):
	for variant in gvc_varians:
		output_file = outpath + '/' +sample_name + '.' + variant + '.vcf'
		print variant
		print feature_dict[variant] , bed_sort_file  , variant ,bam_list, reference, sample_name  ,output_file , version['single_sample_feature2vcf'], 
		print volumes
		ssfJob = single_sample_feature2vcf(feature_dict[variant] , bed_sort_file  , variant ,bam_list, reference, sample_name  ,output_file , version['single_sample_feature2vcf'], volumes)
		
		root.addChild(ssfJob)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("pipeline")



def gvcss_variant_pipeline(root, gvc_lib, reference, dbsnp, bed, outpath,
                           bam_list, segmentSize, sample_name, version,
                           volumes, check_volumes):
    gvc_varians = ['snv', 'indel', 'sv']

    if not os.path.exists(reference + '.fai'):
        logger.error("please samtools faidx{}".format(reference))

    if bed:
        bed_sort_file = os.path.join(outpath, os.path.basename(bed) + '.sort')
        bed_check_sort_reg(reference, bed, bed_sort_file)

    temp = os.path.join(outpath, 'tmp') + '/'

    if not os.path.exists(temp):
        os.makedirs(temp)
    root = root.encapsulate()


    feature_dict = gvc_pipeline(root,
                                reference,
                                segmentSize,
                                bam_list,
                                temp,
                                sample_name,
                                version,
                                check_volumes,
                                gvc_varians,
                                rm_gvcs=True,
                                dbsnp=dbsnp,
                                ccd=bed_sort_file,
                                limit_regions=None)
    qc_pipeline(root, temp, outpath, 'Panel', bam_list, ['T'], reference,
                bed_sort_file, sample_name, version, volumes)

    root = root.encapsulate()



    single_sample_feature2vcf_pipeline (root, feature_dict, bed_sort_file, gvc_varians ,bam_list[0] , reference , sample_name , outpath, version, volumes )

    info = ssinfo_interface.ssInfoInterface()
    for variant in gvc_varians:
        output_file = outpath + '/' +sample_name + '.' + variant + '.vcf'
        info.set_vcf(variant, output_file)
	
    info.set_bam(re.sub('.dup.bam', '.bam', bam_list[0]))
#    svbamPath = os.path.dirname(os.path.realpath(outpath))
    svbamfile = outpath + '/' + sample_name + '.genefuse.bam'
    info.set_SVbam(svbamfile)

    ssinfo = ssinfo_interface.ssInfoInterface()
    GVC_result_dict = ssinfo.get_info()
        
    print GVC_result_dict

    print GVC_result_dict['bam']
    print GVC_result_dict['snv']
    print GVC_result_dict['sv']
    print GVC_result_dict['indel']
############    
    print GVC_result_dict['svbam']

    return root

