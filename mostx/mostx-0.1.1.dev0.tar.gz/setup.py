# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mostx', 'mostx.langs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mostx',
    'version': '0.1.1.dev0',
    'description': 'Quiz Generator',
    'long_description': "# Mostx : Quiz Generator\n\nGenerates the following quiz.\n\n```text\nB is slower than A\nA is faster than C\nB is faster than C\nWhich is the slowest one?\n```\n\nSupports multiple languages.  \n(Japanese, Korean, Traditional-Chinese, English, )\n\n## Installation\n\n```\npip install mostx\n```\n\n## Usage\n\n```python\nimport mostx\n\nprint(sorted(mostx.get_available_langs()))\n# => ['chinese', 'english', 'japanese', 'korean', ]\n\nqgen = mostx.QuizGenerator(lang='english')\nquiz = qgen(choices='ABC', n_adjs=1)\nprint(quiz)\n# Quiz(\n#     statements=[\n#         'C is larger than A',\n#         'A is smaller than B',\n#         'C is larger than B',\n#     ],\n#     question='Which is the smallest?',\n#     choices=('A', 'B', 'C'),\n#     answer='A'\n# )\n```\n\n## etc\n\n[Google App](https://play.google.com/store/apps/details?id=jp.gottadiveintopython.mostx) (Mostx + Kivy)\n",
    'author': 'Nattōsai Mitō',
    'author_email': 'flow4re2c@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gottadiveintopython/mostx',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
