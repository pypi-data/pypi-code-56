#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
#
#  This file is part of power-daps.
#
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.

import setuptools
with open("../../README.md", "r") as fh:
  long_description = fh.read()

print(setuptools.find_packages(where="src"))

setuptools.setup(
  name="power-daps",
  version="0.0.5",
  author="Prasanna Pendse",
  author_email="prasanna.pendse@gmail.com",
  description="A build tool that builds apps in multiple languages",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/power-daps/power-daps",
  install_requires=[
    "power-daps-core==0.0.5",
    "power-daps-meta-model-python-3==0.0.5",
    "power-daps-meta-model-java-9==0.0.5",
    "power-daps-meta-model-rust==0.0.5",
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
