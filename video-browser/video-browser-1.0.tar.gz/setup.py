# Video Browser
# Copyright (C) 2020  Dominik Vilsmeier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path
import re

from setuptools import setup, find_packages


def get_version():
    text = Path('video_browser/__init__.py').read_text()
    return re.findall("^__version__ = '(.+)'$", text, flags=re.M)[0]


setup(
    name='video-browser',
    version=get_version(),
    description='Browse video frames and apply basic transformations.',
    long_description=Path('README.rst').read_text(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Video :: Display',
    ],
    keywords=['video', 'display', 'frames'],
    url='https://gitlab.com/Dominik1123/video-browser',
    author='Dominik Vilsmeier',
    author_email='d.vilsmeier@gsi.de',
    license='GPL-3.0',
    packages=find_packages(),
    install_requires=[
        'arguable',
        'matplotlib',
        'numpy',
        'opencv-python',
        'PyQt5',
    ],
    python_requires='>=3.7',
)
