# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 14:07:45 2020

@author: Aditya Vashista (101703039,TIET)
"""

from distutils.core import setup
setup(
  name = 'missing_AdityaVashista_101703039',        
  packages = ['missing_AdityaVashista_101703039'],   
  version = '0.1',      
  license='MIT',        
  description = 'It is a simple cmd python program that fills missing values in a data set by the median of available values of that attribute column.',   
  author = 'Aditya Vashista, 10703039',              
  author_email = 'aditya.vashista30@gmail.com',      
  url = 'https://github.com/AdityaVashista30/missing_AdityaVashista_101703039',   
  download_url = 'https://github.com/AdityaVashista30/missing_AdityaVashista_101703039/archive/v_0.1.tar.gz',    
  keywords = ['command-line', 'missing','missing data','median','produce data'],
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