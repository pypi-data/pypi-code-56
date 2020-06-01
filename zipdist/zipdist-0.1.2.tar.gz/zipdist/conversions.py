import feather
import pandas as pd
import numpy as np

""" Methods for reading csv/tsv """
def _ndarray_from_csv(fn):
    return np.genfromtxt(fn, delimiter=',')

def _ndarray_from_tsv(fn):
    return np.genfromtxt(fn, delimiter='\t')

def _dataframe_from_csv(fn):
    return pd.read_csv(fn, sep= ",")

def _dataframe_from_tsv(fn):
    return pd.read_csv(fn, sep= "\t")

def _dataframe_from_feather(fn, **kwargs):
	"""Write out the binary feather-format for DataFrames."""
	return pd.read_feather(fn, **kwargs)

def _dataframe_to_feather(df, fn, **kwargs):
	"""Write out the binary feather-format for DataFrames."""
	return df.to_feather(fn, **kwargs)

def _ndarray_to_csv(arr, fn):
	assert fn.endswith(".csv")
	arr.tofile(file = fn, sep = ",")

def _ndarray_to_npy(arr, fn):
	assert fn.endswith(".npy")
	np.save(fn, arr)

def _ndarray_from_npy(fn):
	shape, dtype = get_shape_and_dtype(fn)
	return np.load(fn) #.reshape(shape)

def get_shape_and_dtype(fn):
	with open(fn, 'rb') as npybinary:
		version = np.lib.format.read_magic(npybinary)
		shape, fortran, dtype = np.lib.format._read_array_header(npybinary, version)
		return (shape, dtype) 



# Keep this example comment for now becauesit is a 
# useful concept for not extracting all, but inspecting within .zip file

# import numpy as np
# import zipfile

# def npz_headers(npz):
#     """Takes a path to an .npz file, which is a Zip archive of .npy files.
#     Generates a sequence of (name, shape, np.dtype).
#     """
#     with zipfile.ZipFile(npz) as archive:
#         for name in archive.namelist():
#             if not name.endswith('.npy'):
#                 continue

#             npy = archive.open(name)
#             version = np.lib.format.read_magic(npy)
#             shape, fortran, dtype = np.lib.format._read_array_header(npy, version)
#             yield name[:-4], shape, dtype