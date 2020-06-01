from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="djangodeployer",
    version="0.1.2",
    author="Hristo Mavrodiev",
    author_email="h.mavrodiev@abv.bg",
    description="Deploy django project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    package_data={
        'dj_config': ['djangodeployer/default_config.json'],
    },
    entry_points={
        'console_scripts': [
            'djangodeployer=djangodeployer.cmd_listener:main'
        ]
    }
)
