# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['main']
install_requires = \
['parsel>=1.6.0,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['bilibili-image = main:main']}

setup_kwargs = {
    'name': 'bilibili-image',
    'version': '0.1.3',
    'description': '命令行下载bilibili封面图片',
    'long_description': '# 命令行下载 bilibili 封面图片\n\n安装\n\n```bash\npip install bilibili-image\n```\n\n下载到当前目录并使用默认文件名\n\n```bash\nbilibili-image video_url\n```\n\n指定文件下载路径\n\n```bash\nbilibili-image video_url filepath\n```',
    'author': 'guaifish',
    'author_email': 'guaifish@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guaifish/bilibili-image.git',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
