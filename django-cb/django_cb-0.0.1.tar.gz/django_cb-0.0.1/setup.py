from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

VERSION = '0.0.1'

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# reading requirements from requirements.txt
dir_path = path.dirname(path.realpath(__file__))
reqs_file = 'requirements.txt'.format(dir_path)

with open(reqs_file) as f:
    required = f.read().splitlines()

setup_required = list(required)

setup(
    name='django_cb',
    version=VERSION,
    description='Couchbase NoSQL Django ORM Extension',
    # long_description=long_description,
    # long_description_content_type='text/x-rst',
    url='https://github.com//django-cb',
    setup_requires=setup_required,
    install_requires=required,
    author='Inteliro',
    author_email='jake@inteliro.com',
    classifiers=[],  # i shouldn't need this since it's just local but we'll see
    keywords="",  # once again shouldn't need this but i'll leave it for now
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6',
    include_package_data=True
)
