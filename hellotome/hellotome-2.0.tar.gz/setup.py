import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name = 'hellotome',
    packages = ['hellotome'],
    version = '2.0',
    description = 'Package to get a personalized greeting',
    long_description=README,
    long_description_content_type='text/markdown',
    author = 'Vicente Gutiérrez',
    author_email = 'vinzegtz@gmail.com',
    url = 'https://github.com/vinzegtz/hellotome',
    download_url = 'https://github.com/vinzegtz/hellotome/archive/v2.0.tar.gz',
    keywords = ['hello-world', 'hello', 'greeting'],
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)