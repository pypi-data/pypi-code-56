# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetrytest']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.4.2,<6.0.0', 'requests>=2.23.0,<3.0.0', 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'poetrytest',
    'version': '0.1.0',
    'description': 'poetry 测试用',
    'long_description': '# poetryTest\npytest 接口自动化测试poetry测试用\n',
    'author': 'MonNet',
    'author_email': '250021520@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mongnet/poetryTest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
