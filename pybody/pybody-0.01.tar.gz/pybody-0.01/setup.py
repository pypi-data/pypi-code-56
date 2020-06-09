from distutils.core import setup

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
  name = 'pybody',
  packages = ['pybody'],
  version = '0.01',     
  license='MIT',
  description = 'Python N-Body codes',
  long_description = long_description,
  author = 'Dang Pham',
  author_email = 'dang.c.pham@hotmail.com',
  url = 'https://github.com/dangcpham/pybody',
  keywords = ['nbody','physics'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Physics',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
