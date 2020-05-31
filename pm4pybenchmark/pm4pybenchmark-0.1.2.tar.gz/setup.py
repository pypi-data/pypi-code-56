from os.path import dirname, join

from setuptools import setup

import pm4pybenchmark

def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()

setup(
    name=pm4pybenchmark.__name__,
    version=pm4pybenchmark.__version__,
    description=pm4pybenchmark.__doc__.strip(),
    long_description=read_file('README.md'),
    author=pm4pybenchmark.__author__,
    author_email=pm4pybenchmark.__author_email__,
    py_modules=[pm4pybenchmark.__name__],
    include_package_data=True,
    packages=['pm4pybenchmark'],
    url='http://www.pm4py.org',
    license='GPL 3.0',
    install_requires=[
        "pm4py>=1.3.1",
        "requests"
    ],
    project_urls={
        'Documentation': 'http://pm4py.pads.rwth-aachen.de/documentation/',
        'Source': 'https://github.com/pm4py/pm4py-source',
        'Tracker': 'https://github.com/pm4py/pm4py-source/issues',
    }
)
