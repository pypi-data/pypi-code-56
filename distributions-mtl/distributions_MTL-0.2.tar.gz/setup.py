from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='distributions_MTL',
      version='0.2',
      description='Gaussian distributions',
      long_description =long_description,
      packages=['distributions_MTL'],
      author= 'Matt LaDuke',
      email = 'mladuke@mladuke.com',
      zip_safe=False)
