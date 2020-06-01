from setuptools import setup, find_packages

setup(name='geo-parallel',
      version='0.1.1',
      license='MIT',
      author='Artur Lukin',
      author_email='arhursvaz@gmail.com',
      packages=find_packages(exclude=['tests']),
      zip_safe=False)