from setuptools import setup

with open("README.md","r") as fh:
    long_description_thp = fh.read()

setup(
    name='thp_package',
    version='0.0.1',
    description='Weather Monitoring',
    long_description=long_description_thp,
    url='',
    author='Prabhu Prasad Biswal',
    author_email='prabhuprasadbiswal5@gmail.com',
    license='MIT',
    packages=['thp_package'],
    install_requires=['pandas','numpy'],
    python_requires='>=3.7'
)
