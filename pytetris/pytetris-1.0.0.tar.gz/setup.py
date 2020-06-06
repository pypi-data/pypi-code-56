# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytetris']

package_data = \
{'': ['*'],
 'pytetris': ['assets/font/*',
              'assets/image/*',
              'assets/music/bgm.ogg',
              'assets/music/bgm.ogg',
              'assets/music/bgm.ogg',
              'assets/music/bgm.ogg',
              'assets/music/bgm.ogg',
              'assets/music/bgm.ogg',
              'assets/music/bgm.ogg',
              'assets/music/biu1.ogg',
              'assets/music/biu1.ogg',
              'assets/music/biu1.ogg',
              'assets/music/biu1.ogg',
              'assets/music/biu1.ogg',
              'assets/music/biu1.ogg',
              'assets/music/biu1.ogg',
              'assets/music/biu2.ogg',
              'assets/music/biu2.ogg',
              'assets/music/biu2.ogg',
              'assets/music/biu2.ogg',
              'assets/music/biu2.ogg',
              'assets/music/biu2.ogg',
              'assets/music/biu2.ogg',
              'assets/music/clear.ogg',
              'assets/music/clear.ogg',
              'assets/music/clear.ogg',
              'assets/music/clear.ogg',
              'assets/music/clear.ogg',
              'assets/music/clear.ogg',
              'assets/music/clear.ogg',
              'assets/music/drop.ogg',
              'assets/music/drop.ogg',
              'assets/music/drop.ogg',
              'assets/music/drop.ogg',
              'assets/music/drop.ogg',
              'assets/music/drop.ogg',
              'assets/music/drop.ogg',
              'assets/music/end.ogg',
              'assets/music/end.ogg',
              'assets/music/end.ogg',
              'assets/music/end.ogg',
              'assets/music/end.ogg',
              'assets/music/end.ogg',
              'assets/music/end.ogg',
              'assets/music/start.ogg',
              'assets/music/start.ogg',
              'assets/music/start.ogg',
              'assets/music/start.ogg',
              'assets/music/start.ogg',
              'assets/music/start.ogg',
              'assets/music/start.ogg']}

install_requires = \
['numpy>=1.18.1,<2.0.0', 'pygame>=1.9.6,<2.0.0']

entry_points = \
{'console_scripts': ['game = pytetris.__main__:main']}

setup_kwargs = {
    'name': 'pytetris',
    'version': '1.0.0',
    'description': 'tetris game with ai made by pygame',
    'long_description': '<!--\n * @Author         : yanyongyu\n * @Date           : 2020-05-14 22:26:04\n * @LastEditors    : yanyongyu\n * @LastEditTime   : 2020-06-06 19:13:19\n * @Description    : None\n * @GitHub         : https://github.com/yanyongyu\n-->\n\n# PyTetris\n\n![PyPI](https://img.shields.io/pypi/v/pytetris)\n![GitHub](https://img.shields.io/github/license/yanyongyu/python-tetris)\n![GitHub repo size](https://img.shields.io/github/repo-size/yanyongyu/python-tetris)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/pytetris)\n\n## Table of Contents\n\n- [PyTetris](#pytetris)\n  - [Table of Contents](#table-of-contents)\n  - [Overview](#overview)\n  - [Screenshots](#screenshots)\n  - [Play the Game](#play-the-game)\n    - [Install](#install)\n    - [Start](#start)\n    - [How to Play](#how-to-play)\n  - [Pierre Dellacherie](#pierre-dellacherie)\n    - [Landing Height](#landing-height)\n    - [Eroded Piece Cells Metric](#eroded-piece-cells-metric)\n    - [Board Row Transitions](#board-row-transitions)\n    - [Board Column Transitions](#board-column-transitions)\n    - [Board Buried Holes](#board-buried-holes)\n    - [Board Wells](#board-wells)\n    - [Total](#total)\n    - [Priority](#priority)\n    - [Result Preview](#result-preview)\n  - [Project Development Setup](#project-development-setup)\n\n## Overview\n\nSimple tetris game made by pygame\n\nInspired by [react-tetris](https://github.com/chvin/react-tetris)\n\nAI algorithm: Pierre Dellacherie ([El-Tetris](https://imake.ninja/el-tetris-an-improvement-on-pierre-dellacheries-algorithm/))\n\n## Screenshots\n\n<img src="./static/overview1.png" alt="Overview" width="40%">\n<img src="./static/overview2.png" alt="Overview" width="40%">  \n<img src="./static/overview3.png" alt="Overview" width="40%">\n<img src="./static/overview4.png" alt="Overview" width="40%">\n\n## Play the Game\n\n### Install\n\n```shell\npip3 install pytetris\n```\n\n### Start\n\nRun the following command in the environment which you installed the pytetris package or under the project folder:\n\n```shell\npython -m pytetris\n```\n\nor you can run the project in the project folder by\n\n```shell\npoetry run game\n```\n\n### How to Play\n\nIn the home page, you can use `←→` or click the button to change to start level and use `↑↓` to change the start random line number.\n\n- `↑` : Rotate the piece\n- `←→` : Move the piece left or right\n- `↓` : Speed up the piece\n- `SPACE` : Drop down the piece\n- `P` : Pause the game\n- `S` : Mute control\n- `R` : Reset the game (will loss current score)\n- `A` : Make AI on or off\n\n## Pierre Dellacherie\n\nPierre Dellacherie is a one-piece algorithm.\n\nSix main features:\n\n### Landing Height\n\nThe height where the piece is put. Top or center of the piece is both ok.\n\nExample:\n\n:white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::blue_square::white_large_square::white_large_square::white_large_square::white_large_square:  \n:white_large_square::white_large_square::black_large_square::black_large_square::blue_square::blue_square::black_large_square::black_large_square::white_large_square::white_large_square:  \n:black_large_square::black_large_square::black_large_square::black_large_square::blue_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:  \n:black_large_square::white_large_square::white_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n\nHeight: `4` or `3`\n\n### Eroded Piece Cells Metric\n\nThe number of rows eliminated × The number of the squares the piece contributed\n\nExample:\n\n:white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::blue_square::white_large_square::white_large_square::white_large_square::white_large_square:  \n:white_large_square::white_large_square::black_large_square::black_large_square::blue_square::blue_square::black_large_square::black_large_square::white_large_square::white_large_square:  \n:black_large_square::black_large_square::black_large_square::black_large_square::blue_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:  \n:black_large_square::white_large_square::white_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n\nEliminated lines: `1`\n\nContribute: `1`\n\nEroded Piece Cells Metric: `1 × 1 = 1`\n\n### Board Row Transitions\n\nThe total number of row transitions. A row transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.\n\n**Tips:** Both sides of the wall is concerned as filled.\n\nExample:\n\n:negative_squared_cross_mark::white_large_square::white_large_square::black_large_square::black_large_square::white_large_square::white_large_square::black_large_square::black_large_square::white_large_square::white_large_square::negative_squared_cross_mark:\n\nSingle Row Transitions: `6`\n\n### Board Column Transitions\n\nThe total number of column transitions. A column transition occurs when an empty cell is adjacent to a filled cell on the same column and vice versa.\n\n**Tips:** Both sides of the wall is concerned as filled.\n\nExample:\n\n:negative_squared_cross_mark:  \n:white_large_square:  \n:black_large_square:  \n:black_large_square:  \n:white_large_square:  \n:black_large_square:  \n:negative_squared_cross_mark:\n\nSingle Column Transitions: `4`\n\n### Board Buried Holes\n\nThe total number of column holes. A hole is an empty cell that has at least one filled cell above it in the same column.\n\nExample:\n\n:white_large_square:  \n:black_large_square:  \n:black_large_square:  \n:white_large_square:  \n:black_large_square:\n\nSingle Column Holes: `1`\n\n### Board Wells\n\nThe total number of column wells. A well is a succession of empty cells such that their left cells and right cells are both filled.\n\n**Tips:** As long as there are filled cells on both sides, the empty cell is concerned as well.\n\nExample:\n\n:white_large_square::white_large_square::black_large_square:  \n:black_large_square::white_large_square::black_large_square:  \n:black_large_square::black_large_square::black_large_square:  \n:black_large_square::white_large_square::black_large_square:  \n:black_large_square::white_large_square::black_large_square:\n\nWells: `(1) + (1+2) = 4`\n\n### Total\n\nThe evaluation function is a linear sum of all the above features. Bigger value will be better.\n\n| Feature                   | Weight              |\n| ------------------------- | ------------------- |\n| Landing Height            | -4.500158825082766  |\n| Eroded Piece Cells Metric | 3.4181268101392694  |\n| Board Row Transitions     | -3.2178882868487753 |\n| Board Column Transitions  | -3.2178882868487753 |\n| Board Buried Holes        | -7.899265427351652  |\n| Board Wells               | -3.3855972247263626 |\n\n### Priority\n\npriority = 100 \\* moving_steps + rotation_times\n\nWe choose the action which priority is lower if there are two or more same evaluation actions.\n\n### Result Preview\n\n<img src="./static/ai.gif" width="40%">\n<img src="./static/ai.png" width="40%">\n\n## Project Development Setup\n\nClone the repository then install dependencies.\n\n```shell\npoetry install --no-root\n```\n\nor you can install the dependencies using pip:\n\n```shell\npip3 install pygame numpy\n```\n',
    'author': 'yanyongyu',
    'author_email': 'https://github.com/yanyongyu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yanyongyu/python-tetris',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
