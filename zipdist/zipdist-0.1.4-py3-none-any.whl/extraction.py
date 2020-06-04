import os
import tarfile
import pandas as pd
import numpy as np
import json

class ExtractMachina():
	""" 
	Extaction Machina - return Pandas and NumPy components of .tar.gz archive 
	without extracting the file to disk.
	
	Attributes 
	----------

	Example
	-------
	em = ExtractMachina(dest_tar= "Simpsons.tar.gz")
	em.return_extracted_component(filename = 'lisa.csv', filetype = "pd.DataFrame")

	Notes
	-----
	This is most complicated for .npy files. Where reading from a file handle 
	required using np.frombuffer(fh.read(), dtype = dtype_code) and parsing 
	the header with functions from: numpy/lib/format.py
	"""
	def __init__(self, dest_tar):
		self.dest_tar = dest_tar
		self.dest = dest_tar.replace(".tar.gz", "")

	def return_extracted_component(self, filename, filetype):
		"""
		filename : string
			example 'lisa.csv'
		filetype : string
			must be 'nd.nparray' or 'pd.DataFrame'

		"""
		assert filetype in ['np.ndarray','pd.DataFrame','json'], "filetype arg must be 'np.ndarray' or 'pd.DataFrame' or 'json'"
		assert np.any([filename.endswith(extension) for extension in ['.csv', '.feather', 'npy', 'json']]), "filenames must be .csv, .feather, .json, or .npy" 
		assert os.path.isfile(self.dest_tar), f"{self.dest_tar} file does not exist"

		dest_filename = os.path.join(self.dest, filename)
		with tarfile.open(self.dest_tar) as tar:
			with tar.extractfile(dest_filename) as fh:
				if filetype == "json":
					if filename == "complex_attributes.json":
						complex_attributes = json.load(fh)
						return complex_attributes
					if filename == "simple_attributes.json":
						simple_attributes = json.load(fh)
						return simple_attributes
				if filetype == 'pd.DataFrame':
					if filename.endswith(".feather"):
						return pd.read_feather(fh)
					elif filename.endswith(".csv"):
						return pd.read_csv(fh)
				if filetype == 'np.ndarray':
					if filename.endswith(".npy"):
						#return np.load( file = fh) FAILS: AttributeError: '_FileInFile' object has no attribute 'fileno'
						major, minor = np.lib.format.read_magic(fh)
						# get shape, format, dtype
						shape, fortran, dtype = np.lib.format._read_array_header(fh, version = (major, minor))
						# get serializable dtype
						dtype_code = np.lib.format.dtype_to_descr(dtype)
						return np.frombuffer(fh.read(), dtype = dtype_code).reshape(shape)
					elif filename.endswith(".csv"):
						return np.genfromtxt(fh, delimiter=',')






