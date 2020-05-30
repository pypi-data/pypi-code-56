from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="sebaprinttest",
      version="0.0.2",
      description="Pypi test",
      author="Seba",
      author_email='seba@gmail.com',
      license="GPL 3.0",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/sebastiancuba/sebaprinttest",
      #packages=['enzona_api'],
      packages=find_packages(),
      #install_requires=["requests>=2.23.0", "bs4>=0.0.1", "qrcode>=6.1"],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
      ],
      python_requires='>=3.5',
)