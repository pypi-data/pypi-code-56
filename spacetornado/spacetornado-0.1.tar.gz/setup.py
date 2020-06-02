#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='spacetornado',
      version='0.1',
      description='A minimal Tornado API for Spacy text analytics.',
      author='Wes Bonelli',
      url='https://github.com/w-bonelli/spacetornado',
      packages=['spacetornado'],
      entry_points={
        'console_scripts':[
            'spacetornado = spacetornado.spacetornado:space_tornado'
        ]
      },
      install_requires=['tornado','spacy'])
