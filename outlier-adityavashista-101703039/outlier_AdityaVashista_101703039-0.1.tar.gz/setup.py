# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:14:57 2020

@author: Hp
"""

from distutils.core import setup
setup(
  name = 'outlier_AdityaVashista_101703039',        
  packages = ['outlier_AdityaVashista_101703039'],   
  version = '0.1',      
  license='MIT',        
  description = 'It is an outlier detection and removal cmd program that detects outliers in a given file and stores outlier free data in a new file. It uses IQR method to do so',   
  author = 'Aditya Vashista, 10703039',              
  author_email = 'aditya.vashista30@gmail.com',      
  url = 'https://github.com/AdityaVashista30/outlier_AdityaVashista_101703039',   
  download_url = 'https://github.com/AdityaVashista30/outlier_AdityaVashista_101703039/archive/v_0.1.tar.gz',    
  keywords = ['command-line', 'outlier', 'outlier removal','data cleaning','IQR'],
  install_requires=[            
          'pandas',
          'sys',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.6',
  ],
  python_requires='>=3.6',
)
