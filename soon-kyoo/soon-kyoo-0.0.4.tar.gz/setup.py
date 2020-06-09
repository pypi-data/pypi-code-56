"""This setup.py adapted from
https://github.com/kennethreitz/setup.py/blob/master/setup.py
"""

import pathlib

from setuptools import find_packages, setup


# Package meta-data.
NAME = 'soon-kyoo'
DESCRIPTION = 'A subprocess-based task queue.'
AUTHOR = 'Nathaniel Jones'
EMAIL = 'nathaniel.j.jones@wsu.edu'
URL = 'https://github.com/n8jhj/soon-kyoo'
VERSION = ''  # Use version specified in __version__.py
REQUIRES_PYTHON = '>=3.6.0'

REQUIRED = [
    'Click',
]

ENTRY_POINTS = '''
    [console_scripts]
    soon-kyoo=soon_kyoo.cli.soon_kyoo:soon_kyoo
    sk=soon_kyoo.cli.soon_kyoo:soon_kyoo
'''

here = pathlib.Path(__file__).parent

# Import the README and use it as the long-description.
# NOTE: this will only work if 'README.md' is present in the MANIFEST.in
# file.
try:
    with open(here / 'README.md', encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(here / project_slug / '__version__.py') as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    version=about['__version__'],
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRED,
    entry_points=ENTRY_POINTS,
    license='BSD',
    classifiers=[
        # Trove classifiers.
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
