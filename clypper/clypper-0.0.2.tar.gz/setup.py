# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clypper']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'moviepy>=1.0.3,<2.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'pytube3>=9.6.4,<10.0.0',
 'sh>=1.13.1,<2.0.0',
 'tqdm>=4.46.0,<5.0.0']

entry_points = \
{'console_scripts': ['clypper = clypper:main']}

setup_kwargs = {
    'name': 'clypper',
    'version': '0.0.2',
    'description': 'Rapidly create supercuts from various video sources.',
    'long_description': '# clypper\n\n[![image](https://img.shields.io/pypi/v/clypper.svg)](https://pypi.python.org/pypi/clypper)\n\nRapidly create supercuts from various video sources.\n\n\n## Installation\n\n```python\npip install clypper\n```\n\n\n## Usage\n\nA text file specifying the video source url as well as start and end timestamps can be converted to a supercut using a single command:\n\n```bash\n$ cat input.txt\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ 0:43 0:44\nhttps://www.youtube.com/watch?v=o0u4M6vppCI 1:55 1:59\n$ clypper -i input.txt -o supercut.mp4\n[..]\n$ file supercut.mp4\nsupercut.mp4: ISO Media, MP4 Base Media v1 [IS0 14496-12:2003]\n```\n\n\n## Developer notes\n\n### Making a new release\n\n```bash\n$ bump2version patch # minor major\n$ poetry publish --build\n```\n',
    'author': 'kpj',
    'author_email': 'kpjkpjkpjkpjkpjkpj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpj/clypper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
