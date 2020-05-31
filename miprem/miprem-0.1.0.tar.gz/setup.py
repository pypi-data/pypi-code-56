# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['miprem']

package_data = \
{'': ['*']}

install_requires = \
['cairosvg>=2.4,<3.0',
 'colorclass>=2.2,<3.0',
 'lxml>=4.5,<5.0',
 'terminaltables>=3.1,<4.0']

entry_points = \
{'console_scripts': ['miprem = miprem.main:cli']}

setup_kwargs = {
    'name': 'miprem',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Miprem\n\n_A **m**er**i**t **p**rofile **re**nderer for **m**ajority judgment._\n\nThis project aims to generate vector and bitmap images representing the merit profile of a\n[majority judgment](https://en.wikipedia.org/wiki/Majority_judgment) election, based on the merit profile raw data.\nMiprem does not process poll results, it just render as pretty as possible.\n\n*This project is under active development - installation and usage will rapidly evolve.*\n\n![](tests/sample.svg)\n\n## Installation\n\n```\ncurl https://framagit.org/roipoussiere/miprem/-/archive/master/miprem-master.tar.gz | tar -zx -C miprem\ncd miprem\npip install --user\n```\n\n## Usage\n\nGenerate the image\n\n```\nmiprem > merit_profile.svg\n```\n\nYou can the view the merit profile with your favorite vector image renderer, for instance:\n\n```\nfirefox merit_profile.svg\n```\n\n## Contributing\n\nWoohoo thanks! Please read the [contribution guide](./CONTRIBUTING.md).\n\n## Licence & authorship\n\nThis project is published under [MIT licence](./LICENCE) and developed by Nathanaël Jourdane & contributors\n([maybe you?](./CONTRIBUTING.md)).\n',
    'author': 'Nathanaël Jourdane',
    'author_email': 'roipoussiere@protonmail.com',
    'url': 'https://framagit.org/roipoussiere/miprem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
