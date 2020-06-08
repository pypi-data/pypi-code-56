'''
Author: Krishna
MailID: kvrks@outlook.com
'''

from dataclasses import dataclass
from datetime import datetime
from glob import glob
from os import path, scandir, walk


@dataclass
class FileInfo:
	path: str
	name: str
	size: str
	time: datetime
	text: str
	
	
def translate_bytes(size_in_bytes):
	size = size_in_bytes
	size_unit_list = [' B', ' KB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB']
	'''
	 B : Byte
	KB : Kilobyte
	MB : Megabyte
	GB : Gigabyte
	TB : Terabyte
	PB : Petabyte
	EB : Exabyte
	ZB : Zettabyte
	YB : Yottabyte
	'''
	size_unit_iter = iter(size_unit_list)
	size_unit = next(size_unit_iter)
	while size > 1024.0:
		try:
			size_unit = next(size_unit_iter)
			size /= 1024.0
		except StopIteration:
			break
	return str(round(size,2))+size_unit


def get_files_info(**kwargs):
	directory = kwargs['directory']
	recursively = kwargs['recursively']
	sortbytime = kwargs['sortbytime']
	
	file_info_dict = dict()
	folder_path_list = list()
	folder_path_list.append(directory)
	
	if recursively:
		for r, d, f in walk(directory):
			for folder in d:
				folder_path_list.append(path.join(r, folder))
	
	file_path_list = list()
	for f in folder_path_list:
		for item in scandir(f):
			file_path_list.append(item)
			
	for p in file_path_list:
		try:
			file_stat = p.stat()
			file_size = translate_bytes(file_stat.st_size)
			file_time = datetime.fromtimestamp(file_stat.st_mtime)
			file_info_key = p.path+file_time.strftime('_%d%m%Y%H%M%S')
			file_info_value = FileInfo(p.path,p.name,file_size,file_time,'Information')
			file_info_dict[file_info_key]=file_info_value
		except Exception as e:
			file_info_key = p.path
			file_info_value = FileInfo(p.path,p.name,'-',datetime.now(),'Exception Unable retrive details. May be file got moved from it\'s path')
			file_info_dict[file_info_key]=file_info_value

	if sortbytime:
		file_info_value_list = list(file_info_dict.values())
		file_info_value_list.sort(key=lambda x: x.time, reverse=True)
		file_info_dict = dict()
		for f in file_info_value_list:
			file_info_dict[f.path+f.time.strftime('_%d%m%Y%H%M%S')]=f
	
	return file_info_dict
