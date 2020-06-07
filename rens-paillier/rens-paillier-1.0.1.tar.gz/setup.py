import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'paillier', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open("Description.rst", "rb") as f:
    readme = f.read().decode("utf-8")

packages = ['paillier', 'paillier.util']
install_requires = [
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Intended Audience :: Science/Research',
    ],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    packages=packages,
    install_requires=install_requires,
    python_requires='>=3.8',
    download_url="https://gitlab.com/RensOliemans/paillier/-/archive/master/paillier-master.tar.gz",
    project_urls={
        "Source": "https://gitlab.com/RensOliemans/paillier",
        "Tracker": "https://gitlab.com/RensOliemans/paillier/-/issues",
    }
)
