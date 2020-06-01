import os
from setuptools.command.install import install
from setuptools import setup

pkg = 'rmm'
version = '0.0.1'
name = pkg.split('-')[0] if 'cuda' in pkg else pkg

long_description = 'Please install {} via the rapidsai conda channel. See https://rapids.ai/start.html for instructions.'.format(name)


class InstallWrapper(install):

    def run(self):
        raise Exception(long_description)


setup(name=pkg,
      version=version,
      description='',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/rapidsai/dask-cuda',
      author='RAPIDS development team',
      author_email='pypi@rapids.ai',
      license='Apache 2.0',
      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: Database',
          'Topic :: Scientific/Engineering',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      cmdclass={'install': InstallWrapper},
      )

