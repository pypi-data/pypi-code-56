from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long__ = f.read()
setup(
  name = 'lightshare',  
  version = '0.10',
  long_description=long__,
  long_description_content_type='text/markdown',
  license='MIT',     
  description = 'Faster file sharing using sockets. Makes work easier.',  
  author = 'Nannan',              
  author_email = 'nanna7077@gmail.com',
  keywords = ['Filesharing', 'File', 'Sharing'], 
  py_modules=['lightshare'],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
