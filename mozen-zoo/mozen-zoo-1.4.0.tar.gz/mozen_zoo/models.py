#!/usr/bin/python3
import urllib.request
import ssl, glob, h5py
import os

ssl._create_default_https_context = ssl._create_unverified_context

def load(id_model, mode):
	create_local_repository()
	local_repository_files = []
	local_repository_files = glob.glob(currentFolder()+"/local_repository/*.h5")
	#print(local_repository_files)
	local_repository_files = format_path(local_repository_files)
	#print(local_repository_files) #LIST OF LOCAL REPOSITORY'S MODELS
	probable_path = currentFolder()+"/local_repository/{}.h5".format(id_model)

	if probable_path in local_repository_files:		# IF THE MODEL EXISTS IN THE LOCAL REPOSITORY
		print('Loadind model {} from local repository... \n'.format(id_model))
		print('Model {} loaded.  \n'.format(id_model))
		if mode == "r":
			return  load_model_file(probable_path , "r")
		return load_model_file(probable_path , "w")
	else:
		print('Downloadind model {} from remote repository... \n'.format(id_model))
		file_url = 'https://mozen.gltronic.ovh/api/models/download?id={0}'.format(id_model)
		#print(file_url)
		save_path = currentFolder()+"/local_repository/{0}.h5".format(id_model)
		urllib.request.urlretrieve(file_url, save_path)
		print('Model {} downloaded. \n'.format(id_model))
		print(' Model loaded.')
		if mode == "r":
			return  load_model_file(save_path , "r")
		return load_model_file(save_path , "w")

def format_path(list):
	result = []
	for l in list:
		a = l.replace("\\","/")
		b = a.replace("\\","/")
		#print(b)
		result.append(a)
	return result


def load_model_file(file, mode):
	if mode == "r":
		 ref_read = h5py.File(file, "r")
		 return ref_read
	ref_write = h5py.File(file, "w")
	return ref_write

def create_local_repository():
	cwd = currentFolder()
	local_repository  = cwd+"/local_repository"
	#print(local_repository)
	if not os.path.exists(local_repository):
		os.makedirs(local_repository)

def currentFolder():
	cf = os.getcwd()
	return cf.replace("\\","/")


#load("8", "r")