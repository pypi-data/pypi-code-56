# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 23:27:12 2020

@author: Aditya Vashista (101703039,TIET)
"""

from distutils.core import setup
setup(
  name = 'topsis_AdityaVashista_101703039',        
  packages = ['topsis_AdityaVashista_101703039'],   
  version = '0.1',      
  license='MIT',        
  description = 'Topsis package to find the best option among given products depending upon their features and weightage of each feature for product selection',   
  author = 'Aditya Vashista, 10703039',              
  author_email = 'aditya.vashista30@gmail.com',      
  url = 'https://github.com/AdityaVashista30/topsis_AdityaVashista_101703039',   
  download_url = 'https://github.com/AdityaVashista30/topsis_AdityaVashista_101703039/archive/v_0.1.tar.gz',    
  keywords = ['command-line', 'Best Option', 'Topsi','Product selection'],
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