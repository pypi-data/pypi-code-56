import sys
from setuptools import setup


# Be verbose about Python < 3.6 being deprecated.
if sys.version_info < (3, 6):
    print('\n' * 3 + '*' * 64)
    print('lastcast requires Python 3.6+, and might be broken if run with\n'
          'this version of Python.')
    print('*' * 64 + '\n' * 3)


setup(
    name='lastcast',
    version='2.0.0',
    description='Scrobble music to last.fm from Chromecast.',
    author='Erik Price',
    url='https://github.com/erik/lastcast',
    packages=['lastcast'],
    entry_points={
        'console_scripts': [
            'lastcast = lastcast:main',
        ],
    },
    license='MIT',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyChromecast==5.3.0',
        'click==6.7',
        'pylast==1.7.0',
        'toml==0.9.4',
    ]
)
