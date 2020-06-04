'''
Generate JSON tables containing links to relevant cell
atlas reference datasets and pretrained model weights.
Update the directories on a specified GCS bucket.
'''
import os
import os.path as osp
import subprocess
import json
from typing import List

# Name of the GCS bucket where we store data
GCS_BUCKET = 'calico-website-scnym-storage'
# Path for temporary files
TMP_PATH   = './tmp'
# subdirs in the GCS_BUCKET
PRETRAINED_WEIGHT_PATH = 'pretrained_weights'
REFERENCE_DATA_PATH = 'reference_data'
# species we provide references for
SPECIES = ('human', 'mouse', 'rat',)

def get_gcs_weight_files() -> List[str]:
    '''List all weights on the GCS bucket'''
    o = subprocess.run(
        [
            'gsutil', 
            'ls', 
            f'gs://{GCS_BUCKET}/{PRETRAINED_WEIGHT_PATH}',
        ], 
        stdout=subprocess.PIPE,
    )
    stdout = o.stdout.decode('utf-8').split('\n')
    stdout = [
        x for x in stdout if len(x) > 0
    ]
    return stdout


def get_gcs_model_param_files() -> List[str]:
    '''List all model parameter files on the GCS bucket'''
    o = subprocess.run(
        [
            'gsutil', 
            'ls', 
            f'gs://{GCS_BUCKET}/{PRETRAINED_WEIGHT_PATH}/model_params/',
        ], 
        stdout=subprocess.PIPE,
    )
    stdout = o.stdout.decode('utf-8').split('\n')
    stdout = [
        x for x in stdout if len(x) > 0
    ]
    return stdout


def get_gcs_reference_files() -> List[str]:
    '''List all weights on the GCS bucket'''
    o = subprocess.run(
        [
            'gsutil', 
            'ls', 
            f'gs://{GCS_BUCKET}/{REFERENCE_DATA_PATH}',
        ], 
        stdout=subprocess.PIPE,
    )
    stdout = o.stdout.decode('utf-8').split('\n')
    stdout = [
        x for x in stdout if len(x) > 0
    ]
    return stdout


def gcs2url(gcs_path: str) -> str:
    '''Convert GCS paths to public URLs'''
    bucket_name = gcs_path.split('gs://')[1].split('/')[0]
    file_path = gcs_path.split('gs://')[1].split('/')[1:]
    file_path = '/'.join(file_path)
    url = f'https://storage.googleapis.com/{bucket_name}/{file_path}'
    return url


def make_weights_dict() -> dict:
    weight_paths = get_gcs_weight_files()
    weight_urls = [
        gcs2url(x) for x in weight_paths
    ]
    
    weights_dict = {}
    
    for s in SPECIES + ('results',):
        url = [x for x in weight_urls if s in x]
        # assert only one path exists for each species
        assert len(url) == 1
        weights_dict[s] = url[0]
        
    # add model parameters to the weights
    model_param_paths = get_gcs_model_param_files()
    model_param_urls = [
        gcs2url(x) for x in model_param_paths
    ]
    
    weights_dict['model_params'] = {}
    for s in SPECIES:
        gene_names = [
            x for x in model_param_urls if s in x and 'gene_names' in x
        ]
        class_names = [
            x for x in model_param_urls if s in x and 'cell_types' in x
        ]
        assert len(gene_names) == 1
        assert len(class_names) == 1
        weights_dict['model_params'][s] = {}
        weights_dict['model_params'][s]['gene_names'] = gene_names[0]
        weights_dict['model_params'][s]['class_names'] = class_names[0]
    
    return weights_dict


def make_reference_dict():
    reference_paths = get_gcs_reference_files()
    reference_urls = [
        gcs2url(x) for x in reference_paths
    ]
    
    reference_dict = {}
    for s in SPECIES:
        url = [x for x in reference_urls if s in x]
        # assert only one path exists for each species
        assert len(url) == 1
        reference_dict[s] = url[0]

    return reference_dict


def main():
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    weights_dict   = make_weights_dict()
    reference_dict = make_reference_dict()
    print('weights')
    pp.pprint(weights_dict)
    print('references')
    pp.pprint(reference_dict)
    
    # save to JSONs
    with open('./pretrained_weights.json', 'w') as f:
        json.dump(weights_dict, f)    
    with open('./cell_atlas.json', 'w') as f:
        json.dump(reference_dict, f)
        
    # copy to GCS
    subprocess.run(
        [
            'gsutil',
            'cp',
            'pretrained_weights.json',
            f'gs://{GCS_BUCKET}/link_tables/pretrained_weights.json',
        ]
    )
    subprocess.run(
        [
            'gsutil',
            'cp',
            'cell_atlas.json',
            f'gs://{GCS_BUCKET}/link_tables/cell_atlas.json',
        ]
    )
    
    # make public
    subprocess.run(
        [
            'gsutil',
            'acl',
            'ch',
            '-u',
            'AllUsers:R',
            f'gs://{GCS_BUCKET}/link_tables/pretrained_weights.json',
        ]
    )    
    subprocess.run(
        [
            'gsutil',
            'acl',
            'ch',
            '-u',
            'AllUsers:R',
            f'gs://{GCS_BUCKET}/link_tables/cell_atlas.json',
        ]
    )
    
    return


if __name__ == '__main__':
    main()