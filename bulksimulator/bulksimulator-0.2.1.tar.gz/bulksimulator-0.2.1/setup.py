from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='bulksimulator',
    version='0.2.1',
    description='Module to run a simulation for many parameter choices',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='Jeremy Worsfold',
    author_email='jw3286@bath.ac.uk',
    url='https://github.bath.ac.uk/jw3286/bulksimulator',
    license=license,
    package_dir={'': 'bulksimulator'},
    packages=find_packages(exclude=('tests'))
)