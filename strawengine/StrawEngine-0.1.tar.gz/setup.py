from distutils.core import setup
setup(
  name = 'StrawEngine',
  packages = ['StrawEngine'],
  version = '0.1',
  license='MIT',
  description = 'An advanced template engine',
  author = 'Ben Timor',
  author_email = 'me@bentimor.com', 
  url = 'https://github.com/DrBenana/Straw',  
  download_url = 'https://github.com/DrBenana/Straw/archive/v0.1-beta.tar.gz',
  keywords = ['straw', 'template', 'engine', 'html', 'generator', 'website'],
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  entry_points={
    "console_scripts": [
        "straw=StrawEngine.straw:main",
    ]
  },
)