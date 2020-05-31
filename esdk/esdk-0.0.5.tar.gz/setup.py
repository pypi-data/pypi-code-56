from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="esdk",
      version="0.0.5",
      description="Etecsa sdk",
      author="Sebastian Ricardo Rodriguez Mendez",
      author_email='sebastian.rodriguez@etecsa.cu',
      license="GPL 3.0",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/sebastiancuba/esdk",
      
      packages=find_packages(),
      install_requires=[ 
      'requests',
      'validators',
      'pendulum',
      'pyyaml',
      'ua-parser',
      'user-agents'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
      ],
      python_requires='>=3.4',
)