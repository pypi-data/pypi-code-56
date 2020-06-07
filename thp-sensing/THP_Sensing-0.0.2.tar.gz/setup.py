from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name='THP_Sensing',
    version='0.0.2',
    description='Weather Monitoring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Prabhuprasadbiswal',
    author='Prabhu Prasad Biswal',
    author_email='prabhuprasadbiswal5@gmail.com',
    license='IISERm',
    packages=['THP_Sensing'],
    keywords=['weather','Temperature','Pressure','Humidity'],
    install_requires=['pandas','numpy','sense-hat','matplotlib'],
    python_requires='>=3.7',
)