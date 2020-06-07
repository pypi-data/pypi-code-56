'''
Author: Krishna
Mobile: +917993668960
MailID:	kvrks@outlook.com
Liscense: MIT
'''
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

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
	file_info_dict = dict()
	path = Path(directory)
	path_list = list()
	if recursively:
		path_list = path.rglob('*')
	else:
		path_list = path.glob('*')
	for p in path_list:
		if p.is_file():
			try:
				file_stat = p.stat()
				file_size = translate_bytes(file_stat.st_size)
				file_time = datetime.fromtimestamp(file_stat.st_mtime)
				file_info_key = str(p)+file_time.strftime('_%d%m%Y%H%M%S')
				file_info_value = FileInfo(str(p),p.name,file_size,file_time,'Information')
				file_info_dict[file_info_key]=file_info_value
			except Exception as e:
				file_info_key = str(p)
				file_info_value = FileInfo(str(p),p.name,'-',datetime.now(),'Exception Unable retrive details. May be file got moved from it\'s path')
				file_info_dict[file_info_key]=file_info_value			
	return file_info_dict


'''
# Usage For Your Reference

if __name__=='__main__':

	# Retrieves files information from sub-directories too
	file_info_dict = get_files_info(directory='/home/krishna/mygit-repos/',recursively=True)
	for k,v in file_info_dict.items():
		print(k)
		print(v)
	
	# Doesn't retrieve files information from sub-directories
	file_info_dict = get_files_info(directory='/home/krishna/mygit-repos/',recursively=False)
	for k,v in file_info_dict.items():
		print(k)
		print(v)
'''
