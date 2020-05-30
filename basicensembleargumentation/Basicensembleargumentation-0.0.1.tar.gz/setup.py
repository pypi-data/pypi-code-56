import sys
from setuptools import setup, find_packages

with open('README.md') as f:
    long_desc = f.read()

if sys.version_info < (3, 8):
    print('EnsArg requires at least Python 3.5 to run reliably.')

install_requires = [
    'matplotlib',
    'numpy',
    'pandas',
    'sklearn'
    
]

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Basicensembleargumentation',
    version='0.0.1',
    description='A basic argumentation process where the outcomes from different models can argue for generating a final output.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Istiak Ahmed',
    author_email='istiak.uiu.bd@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keyword='ensembleargumentation',
     project_urls={
        "Code": "https://github.com/Istiak1992/BasicEnsembleArgumentation/",
    },
    packages=find_packages(),
    python_requires=">=3.8"
   
        

)