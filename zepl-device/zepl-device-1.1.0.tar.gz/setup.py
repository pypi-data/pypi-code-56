from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zepl-device",
    version="1.1.0",
    license = 'AGPL-3.0-or-later',
    author="Leonard Pollak",
    author_email="leonardp@tr-host.de",
    description="Zepl Devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/zepl1/zepl-device",
    python_requires='>=3.7',
    install_requires=['pyzmq', 'websockets'],
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src')
)
