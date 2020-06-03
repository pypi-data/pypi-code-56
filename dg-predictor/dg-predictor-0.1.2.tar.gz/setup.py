# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import io
import re

with open('README.md', 'r') as f:
    readme = f.read()

with io.open("src/dg_predictor/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='dg-predictor',
    version=version,
    description='ForAll',
    long_description=readme,
    author='muzi',
    author_email='muzi@gmail.com',
    url='https://github.com/user/dg_predictor',
    license='MIT License',
    platform='linux',
    zip_safe=False,
    packages=find_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=["opencv-python", "numpy", "pyyaml"],
    entry_points={"console_scripts": ["dg-predictor = dg_predictor.predictor:main"]},
)
