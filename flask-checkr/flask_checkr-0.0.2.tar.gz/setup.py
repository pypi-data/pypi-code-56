from setuptools import setup, find_packages
from flask_checkr import __version__

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='flask_checkr',
    version=__version__,
    license='MIT',
    author='Pavel Pascari',
    author_email='pascaripavel@gmail.com',
    url='https://github.com/pavelpascari/flask-checkr',
    download_url="https://github.com/pavelpascari/flask-checkr/archive/v%s.tar.gz" % __version__,
    description='Easily validate Flask requests with JSONSchema.',
    long_description=long_description,
    platforms=['OS Independent'],
    install_requires=[
        'Flask',
        'jsonschema',
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
