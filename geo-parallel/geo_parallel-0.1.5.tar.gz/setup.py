from setuptools import setup, find_packages

setup(name='geo_parallel',
      version='0.1.5',
      license='MIT',
      author='Artur Lukin',
      author_email='arhursvaz@gmail.com',
      packages=find_packages(exclude=['tests']),
      zip_safe=False)