from distutils.util import convert_path

from setuptools import find_packages, setup

DATA_DIR = 'data'

setup(name='MGEdb',
      version='1.0.2',
      description='Mobile Genetic Element database',
      long_description_markdown_filename='README.md',
      long_description_content_type='text/markdown',
      url='https://bitbucket.org/mhkj/mgedb/',
      author='Markus Johansson',
      author_email='markus.johansson@me.com',
      license='GPLv3',
      requires_python='>=3.6',
      include_package_data=True,
      package_data={
          'mgedb': [
              '%s/*.json' % DATA_DIR,
              '%s/*.yml' % DATA_DIR,
              '%s/sequences.d/*.fna' % DATA_DIR,
              '%s/sequences.d/*.faa' % DATA_DIR,
          ],
      },
      entry_points={'console_scripts': ['mgedb=mgedb.cli:main']},
      tests_require=[
          'pytest', 'pytest-cov', 'mypy', 'flake8-bugbear', 'flake8-commas',
          'flake8-comprehensions', 'flake8-docstrings', 'flake8-isort',
          'flake8-polyfill', 'flake8-quotes', 'flake8-todo', 'flake8',
          'setuptools-markdown', 'pytest-runner',
      ],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      packages=find_packages(exclude=('tests',)))
