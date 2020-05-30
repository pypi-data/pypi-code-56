from setuptools import setup,find_packages

setup(
   name='allosaurus',
   version='0.0.7',
   description='a multilingual phone recognizer',
   author='Xinjian Li',
   author_email='xinjianl@cs.cmu.edu',
   url="https://github.com/xinjli/allosaurus",
   packages=find_packages(),
   install_requires=[
      'scipy',
      'numpy',
      'resampy',
      'panphon',
      'torch',
   ]
)