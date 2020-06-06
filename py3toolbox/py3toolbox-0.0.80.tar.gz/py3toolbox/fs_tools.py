import os
import sys
import re
import hashlib
import glob
import gzip
import codecs
import base64

from shutil import copyfile,rmtree
from stat import * 
import time

def rm_folder(folder_name, empty_only=False):
  if empty_only == False:
    rmtree(folder_name,ignore_errors=True)
  else:
    if is_folder(folder_name) == False :
      return
    
    file_list = get_files(folder = folder_name, type='file')
    dir_list  = get_files(folder = folder_name, type='dir')
    for d in dir_list :
      if is_file_exists(d) :
        d_empty = True
        for f in file_list :      
          if f.find(d) == 0 :
            d_empty = False
            break
        if d_empty == True:
          rmtree(d,ignore_errors=True)
        
    
def mk_folder(folder_name) :
  if is_file_exists(folder_name) == False :
    os.makedirs(folder_name, exist_ok=True)

def get_file_folder(file_path) :
  return os.path.dirname (file_path)
  
  
def clean_folder(folder_name):
  if is_file_exists(folder_name) :
    for the_file in os.listdir(folder_name):
      file_path = os.path.join(folder_name, the_file)
      if   os.path.isfile(file_path) : rm_file(file_path)
      elif os.path.isdir(file_path)  : rm_folder(file_path)
  else:
    mk_folder (folder_name)
  
def is_file_exists(file_name):
  return os.path.exists(file_name)
  
def copy_file(src_file,dest_file):
  if is_file_exists(src_file) :  
    mk_folder(get_file_folder(dest_file))
    copyfile(src_file,dest_file)    
  
def rm_file(file_name) :
  if os.path.isfile(file_name): 
    os.remove(file_name)
    
def write_file(file_name, text, mode='w', is_new = False):
  file_folder = get_file_folder(file_name)
  if is_file_exists(file_folder) == False: mk_folder(file_folder)
    
  if is_new == True: rm_file(file_name)
  with codecs.open(file_name, mode, 'utf8') as fh:
    fh.write(text)

def write_log(file_name, text, is_new = False):
  write_file(file_name=file_name, text=text + "\n", mode='a', is_new=is_new)
    
def read_file(file_name, return_type='str'):
  if return_type == 'str' :
    return codecs.open(file_name, 'r', 'utf8').read()
    
  if return_type == 'list' :
    return codecs.open(file_name, 'r', 'utf8' ).readlines() 
    
def get_md5(file_name) :  
  hasher = hashlib.md5()
  with open(file_name, 'rb') as fh:
    buf = fh.read()
    hasher.update(buf)
  return (hasher.hexdigest())

  
def is_file (file) :
  return os.path.isfile(file) 

def is_folder (file) :
  return os.path.isdir(file) 
  
def check_type(full_path):
  if is_file_exists(full_path) : 
    if is_file(full_path) : 
      return 'file'
    elif is_folder(full_path) :  
      return 'dir'
  else:
    return None
  
def gen_files(folder, ext = '', recursive=True, type='all') :
  for f in glob.iglob(folder + '/**/*' + ext , recursive=recursive):
    if os.name=='nt':  
      f = f.replace('\\','/').replace('//','/')
    if type=='all' : 
      yield f
    elif check_type(f) == type : 
      yield f

def get_files(folder, ext='', recursive=True, type='all') : 
  files = []
  for f in gen_files(folder=folder, ext = ext, recursive=recursive, type=type):
    files.append(f)
  return files

def get_file_info(file_name) :
  if is_file_exists(file_name):
    st = os.stat(file_name)
    return { "file_name": file_name, "size" : int(st[ST_SIZE]), "access_time" : st[ST_ATIME] }
  else:
    return None
  
def get_folder_info(folder, recursive=True ):
  total_size  = 0
  total_count = 0
  files = get_files(folder=folder, recursive=recursive)
  total_count = len(files)
  for f in files : 
    total_size += get_file_info(f)["size"]
  
  return (total_count, total_size)  


def do_zip(input_file=None,output_file=None,input_data=None, output="file"):
  """
  usage  : 
    zip compress input file or bytes string or string
    output: file  : save as file
            byte  : return bytes string
  
  examples:
    do_zip(input_file="c:/1.txt",output_file="c:/1.zip")
    do_zip(input_file="c:/1.txt",output="byte")

    do_zip(dest_file="c:/1.zip", input_data="test_string",output="file")
    do_zip(input_data="test_string",output="byte")

  """

  assert output == "file" or  output == "byte" , "Wring output type : should be file or byte"

  # check input 
  if input_file is not None:
    with open(input_file, 'rb') as f_in: 
      input_data = f_in.read()
  elif input_data is not None:
    if type(input_data).__name__ == 'str' :
      input_data =  str.encode(input_data)


  compressed_bytes = gzip.compress(input_data, compresslevel=9)


  if output == "file":
    with open(output_file, 'wb') as f_out: 
      f_out.write(compressed_bytes)
    return output_file
  elif output == "byte":
    return  compressed_bytes

  pass

def do_unzip(input_file=None,output_file=None,input_data=None, output="file"):
  """
  usage  : 
    do_unzip decompress (unzip) input file or bytes string or string
    output: file  : save as file
            byte  : return bytes string
  
  examples:
    do_unzip(input_file="c:/1.zip",dest_file="c:/1.bin")
    do_unzip(input_file="c:/1.zip",output="byte")

    do_unzip(output_file="c:/1.zip", input_data="test_string",output="file")
    do_unzip(input_file="test_string",output="byte")

  """

  assert output == "file" or  output == "byte" , "Wring output type : should be file or byte"

  # check input 
  if input_file is not None:
    with open(input_file, 'rb') as f_in: 
      input_data = f_in.read()
  elif input_data is not None:
    if type(input_data).__name__ == 'str' :
      input_data =  str.encode(input_data)

  decompressed_bytes = gzip.decompress(input_data)

  if output == "file":
    with open(output_file, 'wb') as f_out: 
      f_out.write(decompressed_bytes)
    return output_file
  elif output == "byte":
    return  decompressed_bytes

  pass




def unzip(gzfile) :
  fgz = gzip.GzipFile(gzfile, 'rb')
  binary_content = fgz.read()
  fgz.close()
  return binary_content








def base64_encode(input_file=None,output_file=None,input_data=None, output="file"):
  """
  usage  : 
    base64 encode input file or bytes string or string
    output: file  : save as file
            text  : return bytes string
  
  examples:
    base64_encode(input_file="c:/1.txt",output_file="c:/1.zip")
    base64_encode(input_file="c:/1.txt",output="text")

    base64_encode(dest_file="c:/1.zip", input_data="test_string",output="file")
    base64_encode(input_data="test_string",output="text")

  """
  assert output == "file" or  output == "text" , "Wring output type : should be file or text"
  
  # check input 
  if input_file is not None:
    with open(input_file, 'rb') as f_in: 
      input_data = f_in.read()
  elif input_data is not None:
    if type(input_data).__name__ == 'str' :
      input_data =  str.encode(input_data)

  encoded_bytes = base64.b64encode(input_data)
 
  if output == "file":
    with open(output_file, 'wb') as f_out: 
      f_out.write(encoded_bytes)
    return output_file
  elif output == "text":
    return  encoded_bytes.decode() 

  

def base64_decode(input_file=None,output_file=None,input_data=None, output="file"):
  """
  usage  : 
    base64 decode input file or bytes string or string
    output: file  : save as file
            byte  : return bytes string
  
  examples:
    base64_decode(input_file="c:/1.txt",output_file="c:/1.zip")
    base64_decode(input_file="c:/1.txt",output="byte")

    base64_decode(dest_file="c:/1.zip", input_data="test_string",output="file")
    base64_decode(input_data="test_string",output="byte")

  """
  assert output == "file" or  output == "byte" , "Wring output type : should be file or byte"
  input_text = None

  # check input 
  if input_file is not None:
    with open(input_file, 'rb') as f_in: 
      input_data = f_in.read()

  # convert to ascii
  if type(input_data).__name__ != 'str' :
    input_text =  input_data.decode()
  else:
    input_text = input_data

  assert input_text is not None, "Error of reading input"

  decoded_bytes = base64.b64decode(input_text)
 
  if output == "file":
    with open(output_file, 'wb') as f_out: 
      f_out.write(decoded_bytes)
    return output_file
  elif output == "byte":
    return  decoded_bytes
  

  pass








def reverse_str(text) :
  reversed_txt = text[::-1]
  return reversed_txt



def encrypt(input_file=None,output_file=None):
  zip_data = do_zip(input_file=input_file,output="byte")
  b64_data = base64_encode(input_data=zip_data,output="text")
  r_b64_data = reverse_str(b64_data)
  with open(output_file, 'wt') as f_out: 
    f_out.write(r_b64_data)
    f_out.flush()
  pass

  
def decrypt(input_file=None,output_file=None):
  with open(input_file, 'rt') as f_in: 
    r_b64_data = f_in.read()
  b64_data = reverse_str(r_b64_data)
  b64_decoded_data = base64_decode(input_data=b64_data, output="byte") 
  unzip_data =  do_unzip(input_data=b64_decoded_data, output_file=output_file, output="file")
  pass


def replace_text_files(replace_keys, files, casesesitive=True):
  """
    usage  : replace text in list of files/single file
    params : 
      oldkeys = old keys to be replaced
      newkeys = new keys to replace old one
      type   = text  
      casesesitive = True (default) | False
    returns : 
      dictionary {} includes files which has been changed     

    sample input :
      result = replace_text_files([('a','a_new'), ('b', 'b_xxx')], ['R:/1.txt','R:/2.txt','R:/3.txt'] )
    
    sample output :
      {
       file1: True,  # file1 changed
       file2: False, # file2 NOT changed
       file3: True   # file3 changed
      }

  """

  result = {}
  if isinstance(files, str) :
    files = [files]

  if isinstance(replace_keys, tuple) :
    replace_keys = [replace_keys]

  for f in files :
    f_text = read_file(f,return_type='str')
    result[f] = False
    for oldkey, newkey in replace_keys:
      if casesesitive == True:
        f_text, count = re.subn(oldkey, newkey, f_text)
      else:
        f_text, count = re.subn(oldkey, newkey, f_text,flags = re.IGNORECASE)
      
      if count > 0 : 
        result[f] = True
        write_file(file_name=f, text = f_text, mode="w")

  return result
  
if __name__ == "__main__":
  #print (len( get_files (folder="R:/", type='file')))
  
  #for f in gen_files (folder="R:/", type='file'):
  #  print (f)
  

  #print (base64_encode(input_file="R:/panda.jpg",output_file="R:/panda.jpg.b64", output="text"))
  #print (base64_decode(input_file="R:/panda.jpg.b64",output_file="R:/panda1.jpg", output="text"))
  encrypt(input_file="R:/panda.jpg",output_file="R:/panda.jpg.encrypted")
  
  

  decrypt(input_file="R:/panda.jpg.encrypted",output_file="R:/panda_restored.jpg")
  #rm_folder ("R:/", empty_only=True)
  #print (replace_text_files.__doc__)
  #result = replace_text_files([('http_proxy.*',''), ('b.*', 'BB')], ['R:/1.txt','R:/2.txt','R:/3.txt'],casesesitive=False )

  #print (result)

    