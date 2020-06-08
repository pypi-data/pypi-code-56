# -*-coding:Utf-8 -*

import os
import sys

import nibabel as nib


resting = sys.argv[1]
seed = sys.argv[2]
mask = sys.argv[3]
res_folder = sys.argv[4]

# verify if we have the right number of parameters
if len(sys.argv) < 5:
    print("usage: python funcon.py resting seed mask res_folder")
    print("resting: the path to your resting state image")
    print("seed: the path to the seed image")
    print("mask: the path to the mask image")
    print("res_folder: the path to your results folder")
    exit()

#import the nifti
i_resting = nib.load(resting)
i_seed = nib.load(seed)
i_mask = nib.load(mask)

#optional image dimension info
i_resting.shape
i_seed.shape
i_mask.shape

#check that the three shapes are the same == or different !=
i_resting.shape[:3]
if i_resting.shape[:3] != i_seed.shape:
    print("seed and restings are not in the same space")
    exit()
if i_resting.shape[:3] != i_mask.shape:
    print("mask and restings are not in the same space")
    exit()




#write the output images
spearman = nib.Nifti1Image(table, i_mask.affine)
res_file = os.path.join(res_folder, 'SpearmanCorr.nii.gz')
nib.save(spearman, res_file)
