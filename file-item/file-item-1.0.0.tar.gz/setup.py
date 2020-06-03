"""
file_item
"""
from setuptools import setup, find_packages

from file_item import __version__ as version

INSTALL_REQUIRES = [
]

EXTRAS_DEV_TESTFILES_COMMON = [
]

EXTRAS_DEV_LINT = []

EXTRAS_DEV_TEST = [
    "coverage",
    "pytest>=3.10",
]

EXTRAS_DEV_DOCS = [
    "readme_renderer",
    "sphinx",
    "sphinx_rtd_theme>=0.4.0",
]

with open('README.rst') as readme:
    r = str(readme.read())

setup(
    name='file-item',
    version=version,
    packages=find_packages(exclude=['*test*']),
    url='https://github.com/dmitriiweb/file-item',
    license='MIT',
    author='Dmitrii K',
    author_email='dmitriik@protonmail.com',
    description='My file-item',
    long_description=r,
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": (EXTRAS_DEV_TESTFILES_COMMON +
                EXTRAS_DEV_LINT +
                EXTRAS_DEV_TEST +
                EXTRAS_DEV_DOCS),
        "dev-lint": (EXTRAS_DEV_TESTFILES_COMMON +
                     EXTRAS_DEV_LINT),
        "dev-test": (EXTRAS_DEV_TESTFILES_COMMON +
                     EXTRAS_DEV_TEST),
        "dev-docs": EXTRAS_DEV_DOCS,
        "timezone": ["pytz"],
    },
    keywords='file-item',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ),
)