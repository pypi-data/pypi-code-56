#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import numpy as np

import nibabel as nib

""" 1) Mask the images by the gray matter mask
2) flatten the disconnectomes into 1D arrays
3) create a matrix to associate every voxel with its gray-disconnectome values
"""

gray_path = "/data/Chris/thr100_bin_avg152T1_gray_2mm.nii.gz"
gray_img = nib.load(gray_path)
grap_data = gray_img.get_data()

disco = ""
