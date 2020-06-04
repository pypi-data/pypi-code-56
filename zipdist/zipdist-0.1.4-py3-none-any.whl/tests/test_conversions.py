import pytest
import numpy as np
import pandas as pd
from zipdist.conversions import _ndarray_to_npy, _ndarray_from_npy, _dataframe_to_feather,_dataframe_from_feather
import os


def test_conversion_array_to_npy():
	test_arr = np.zeros(10)
	test_fn = "fntest.npy"
	_ndarray_to_npy(arr = test_arr, fn= test_fn )
	assert os.path.isfile(test_fn)

test_arrays = [ (np.zeros(10), "np.zeros(10)"),
				(np.ones(10),  "np.ones(10)"),
				(np.array([[0, 1, 2, 3], [4, 5, 6, 7]]), "2D np.array"),
				(np.random.randint(0, 100, size=(30, 10, 2)), "3D np.array") ]

@pytest.mark.parametrize("x,y",test_arrays)
def test_conversion_array_to_npy_to_array_with_shape(x,y):
	assert isinstance(y, str)
	test_arr = x
	test_arr_shape = x.shape
	test_fn = "fntest.npy"
	_ndarray_to_npy( fn= test_fn, arr = test_arr )
	assert os.path.isfile(test_fn)
	rec_arr = _ndarray_from_npy(fn = test_fn)
	assert np.all(test_arr == rec_arr)
	print(test_arr_shape, rec_arr.shape)
	assert np.all(test_arr_shape == rec_arr.shape)

def test_conversion_df_to_feather():
	test_df = pd.DataFrame({"A":[1,3] ,"B":[12,4]})
	test_fn = "testfeather.feather"
	_dataframe_to_feather(df= test_df, fn =test_fn )
	assert os.path.isfile(test_fn)
	rec_df = _dataframe_from_feather(fn = test_fn)
	assert isinstance(rec_df, pd.DataFrame)
	assert np.all(test_df.eq(rec_df))