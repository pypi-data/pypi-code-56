from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='bulksimulator',
    version='0.3.2',
    description='Module to run a simulation for many parameter choices',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jeremy Worsfold',
    author_email='jw3286@bath.ac.uk',
    url='https://github.bath.ac.uk/jw3286/bulksimulator',
    license="GPL3",
    packages=find_packages(exclude=('tests'))
)