import pytest
import numpy as np
import pandas as pd
from zipdist.zip2 import Zipdist2
from zipdist.extraction import ExtractMachina
import os 
import sys

def make_tar_gz():
	class X():
		def __init__(self, name):
			self.name = name

	x = X(name = 'xxx')
	x.year = 2020
	x.exnp = np.zeros(3)
	x.exnp1 = np.zeros(10)#, "np.zeros(10)"
	x.exnp2 = np.ones(10) #,  "np.ones(10)"),
	x.exnp3 = np.array([[0, 1, 2, 3], [4, 5, 6, 7]])#, "2D np.array"),
	x.exnp4 = np.random.randint(0, 100, size=(30, 10, 2))#, "3D np.array") ]
	x.expd = pd.DataFrame({"A":[1,2,3], "B":[2,4,6]})
	z = Zipdist2(name = "xxx", target = x)
	z._save(dest = "xxx", dest_tar = "xxx.tar.gz")
	os.system('rm -rf xxx')
	return x

def test_extraction_on_pdDataFrame_from_csv():
	x = make_tar_gz()
	assert os.path.isfile("xxx.tar.gz")
	em = ExtractMachina(dest_tar= "xxx.tar.gz")
	r = em.return_extracted_component(filename = 'expd.csv', filetype = "pd.DataFrame")
	assert isinstance(r, pd.DataFrame)
	assert "A" in r.columns
	assert "B" in r.columns
	os.system('rm xxx.tar.gz')

def test_extraction_on_pdDataFrame_from_feather():
	x = make_tar_gz()
	assert os.path.isfile("xxx.tar.gz")
	em = ExtractMachina(dest_tar= "xxx.tar.gz")
	r = em.return_extracted_component(filename = 'expd.feather', filetype = "pd.DataFrame")
	assert isinstance(r, pd.DataFrame)
	assert "A" in r.columns
	assert "B" in r.columns
	os.system('rm xxx.tar.gz')

def test_extraction_on_np_ndarray_from_csv():
	x = make_tar_gz()
	assert os.path.isfile("xxx.tar.gz")
	em = ExtractMachina(dest_tar= "xxx.tar.gz")
	r = em.return_extracted_component(filename = 'exnp.csv', filetype = "np.ndarray")
	assert isinstance(r, np.ndarray)
	assert np.array_equal(x.exnp1, em.return_extracted_component(filename = 'exnp1.csv', filetype = "np.ndarray"))
	assert np.array_equal(x.exnp2, em.return_extracted_component(filename = 'exnp2.csv', filetype = "np.ndarray"))
	assert np.array_equal(x.exnp3, em.return_extracted_component(filename = 'exnp3.csv', filetype = "np.ndarray"))
	# TODO : Add >2D arrays to slices in csv with functionality along the lines of Joe Kington https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file       
	# assert np.array_equal(x.exnp4, em.return_extracted_component(filename = 'exnp4.csv', filetype = "np.ndarray")) 
	os.system('rm xxx.tar.gz')

def test_extraction_on_np_ndarray_from_npy():
	x = make_tar_gz()
	assert os.path.isfile("xxx.tar.gz")
	em = ExtractMachina(dest_tar= "xxx.tar.gz")
	r = em.return_extracted_component(filename = 'exnp.npy', filetype = "np.ndarray")
	assert isinstance(r, np.ndarray)
	assert np.array_equal(x.exnp1, em.return_extracted_component(filename = 'exnp1.npy', filetype = "np.ndarray"))
	assert np.array_equal(x.exnp2, em.return_extracted_component(filename = 'exnp2.npy', filetype = "np.ndarray"))
	assert np.array_equal(x.exnp3, em.return_extracted_component(filename = 'exnp3.npy', filetype = "np.ndarray"))
	assert np.array_equal(x.exnp4, em.return_extracted_component(filename = 'exnp4.npy', filetype = "np.ndarray"))
	os.system('rm xxx.tar.gz')


def test_extraction_on_json_simple_attributes():
	x = make_tar_gz()
	assert os.path.isfile("xxx.tar.gz")
	em = ExtractMachina(dest_tar= "xxx.tar.gz")
	r = em.return_extracted_component(filename = 'simple_attributes.json', filetype = "json")
	assert isinstance(r, dict)
	os.system('rm xxx.tar.gz')

def test_extraction_on_json_complex_attributes():
	x = make_tar_gz()
	assert os.path.isfile("xxx.tar.gz")
	em = ExtractMachina(dest_tar= "xxx.tar.gz")
	r = em.return_extracted_component(filename = 'complex_attributes.json', filetype = "json")
	assert isinstance(r, dict)
	os.system('rm xxx.tar.gz')

