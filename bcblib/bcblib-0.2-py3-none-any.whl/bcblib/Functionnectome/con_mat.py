# -*- coding: utf-8 -*-

import os
import numpy as np

import dask.array as da
import dask.dataframe as ddf
import dask
import nibabel as nib
import pandas as pd
from sklearn import decomposition
from nilearn import plotting

path = "/data/Chris/new_disco_party/patient16.nii.gz"
nii = nib.load(path)
data = da.from_array(nii.get_data(), chunks=100)

data.shape
type(data)

tt = da.from_array(np.array([[[1,2], [3,4]], [[5,6],[7,8]]]), chunks=100)
tt.shape
toto = data.flatten()
toto.shape


fmri_path = "/data/Chris/RS_bptf_MNI/patient17.nii.gz"
fmri = nib.load(fmri_path)



fmri_data = fmri.get_data()
# fmri_data = da.from_array(fmri.get_data(), 200)
fmri_data.shape
mat = [fmri_data[:, :, :, i].flatten() for i in range(fmri_data.shape[3])]
mat
mat = np.array(mat)
mat.shape
daska = da.from_array(mat, chunks=100)
cov = da.cov(daska)
cov.shape
g, omega = np.linalg.eig(cov)
g
omega
# dask.dataframe.from_dask_array(fmri_data)

display = plotting.plot_matrix(cov, colorbar=True)
