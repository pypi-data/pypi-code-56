# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imgtopdfeasy']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['img2pdf = imgtopdfeasy:main']}

setup_kwargs = {
    'name': 'imgtopdfeasy',
    'version': '0.1.1',
    'description': 'This is command line utility to convert images in a directory to  PDF file.',
    'long_description': '# Img2pdf [![GitHub license](https://img.shields.io/github/license/naveen521kk/img2pdf)](https://github.com/naveen521kk/img2pdf/blob/master/LICENSE)  [![GitHub stars](https://img.shields.io/github/stars/naveen521kk/img2pdf)](https://github.com/naveen521kk/img2pdf/stargazers)\nThis is command line utility to convert images in a directory to  PDF file.\n\nThis is very simple CLI to convert images in a directory to a PDF file. This use Pillow( PIL ), to achieve this.\n\nTo use this go to the directory where you have images. Then type the commands below.\n\n```sh\ngit clone https://github.com/naveen521kk/img2pdf.git\n```\n\nThis create a folder called `img2pdf`. Then go into the folder by\n\n```sh\ncd img2pdf\n```\n\nAfter that typing \n\n```sh\npip install -r requirements.txt\n```\nwould install necessary Requirements for it to run.\n\nAfter that typing \n```sh\npython img2pdf.py -h\n```\nin your terminal would run the program and show the necessary arguments required like below.\n```ssh\nusage: img2pdf.py [-h] -i INPUT -o OUTPUT -ext EXTENSION\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i INPUT, --input INPUT\n                        Input file folder full path. Realti\n  -o OUTPUT, --output OUTPUT\n                        Output file name,No pdf required\n  -ext EXTENSION, --extension EXTENSION\n                        File extension of image to add.\n```\n\nEach of it are self explanatory.\n\nCrafted with 💓 by Naveen.\n',
    'author': 'Naveen',
    'author_email': 'naveen@syrusdark.website',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/naveen521kk/img2pdf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
