"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='falconify',
    version='0.1.1',
    description='The Scaffolding tool for Falconify',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/raphacosta/falconify-scaffolding',
    author='Raphael Costa',
    author_email='raphagc85@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='falconify tooling development framework falcon',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={
        'falconify': [
            'config.json',
            'Templates/CommandHandler.py.mako',
            'Templates/Model.py.mako',
            'Templates/Repository.py.mako',
            'Templates/RequestHandler.py.mako',
            'Templates/Routes.py.mako',
            'Templates/Transformer.py.mako',
            'Templates/UseCase.py.mako',
        ],
    },
    python_requires='>=3.5, <4',
    entry_points={
        'console_scripts': [
            'falconify=falconify:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://gitlab.com/raphacosta/falconify-scaffolding/-/issues',
        'Source': 'https://gitlab.com/raphacosta/falconify-scaffolding/',
    },
)