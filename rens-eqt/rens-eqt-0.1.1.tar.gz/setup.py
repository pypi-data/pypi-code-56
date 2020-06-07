import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'eqt', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open("Description.rst", "rb") as f:
    readme = f.read().decode("utf-8")

packages = ['eqt', 'eqt.util']
install_requires = [
    'rens-paillier>=0.1',
]

testing_requirements = [
    'coverage==5.0.3',
    'flake8==3.7.9'
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    packages=packages,
    install_requires=install_requires,
    extras_require={
        'testing': testing_requirements,
    },
    python_requires='>=3.8',
)
