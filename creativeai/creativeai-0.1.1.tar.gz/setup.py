# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['creativeai', 'creativeai.image', 'creativeai.image.encoders']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'creativeai',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Alex J. Champandard',
    'author_email': '445208+alexjc@users.noreply.github.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
