from distutils.core import setup
import pathlib
HERE = pathlib.Path(__file__).parent
setup(
  name = 'lightshare',  
  version = '0.9',
  long_description=(HERE/"README.md").read_text(),
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
