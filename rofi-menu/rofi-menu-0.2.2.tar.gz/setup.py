# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rofi_menu', 'rofi_menu.contrib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rofi-menu',
    'version': '0.2.2',
    'description': 'Create rofi menus via python',
    'long_description': '<p align="center">\n    <a href="https://pypi.org/project/rofi-menu/">\n        <img src="https://badge.fury.io/py/rofi-menu.svg" alt="Package version">\n    </a>\n</p>\n\n# rofi-menu\n\nRofi allows defining custom modes ([see the spec](https://github.com/davatorium/rofi/wiki/mode-Specs)).\n\nThis lib is a reference implementation with some extra "sugar".\n\nSimple demo:\n\n![custom menu](https://github.com/miphreal/python-rofi-menu/raw/master/docs/demo.gif)\n\n## Installation\n\nUsing pip\n\n```sh\n$ pip install rofi-menu\n```\n\n## Example\n\nCreate a python script which will be used for rofi mode\ne.g. `example.py` (don\'t forget to mark it as executable -- `chmod +x ./example.py`)\n\nAssuming you installed `rofi-menu` into a virtual environment (let\'s say it\'s `~/.pyenv/versions/rofi/bin/python`).\nMake sure shebang points to the right python executable, e.g. `#!/home/user/pyenv/versions/rofi/bin/python`.\n```python\n#!/home/user/pyenv/versions/rofi/bin/python\nimport rofi_menu\n\n\nclass ProjectsMenu(rofi_menu.Menu):\n    prompt = "Projects"\n    items = [\n        rofi_menu.BackItem(),\n        rofi_menu.ShellItem("Project 1", "code-insiders ~/Develop/project1"),\n        rofi_menu.ShellItem("Project 2", "code-insiders ~/Develop/project2"),\n        rofi_menu.ShellItem("Project X", "code-insiders ~/Develop/projectx"),\n    ]\n\n\nclass LogoutMenu(rofi_menu.Menu):\n    prompt = "Logout"\n    items = [\n        rofi_menu.ShellItem("Yes", "i3-msg exit", flags={rofi_menu.FLAG_STYLE_URGENT}),\n        rofi_menu.ExitItem("No", flags={rofi_menu.FLAG_STYLE_ACTIVE}),\n    ]\n\n\nclass MainMenu(rofi_menu.Menu):\n    prompt = "menu"\n    items = [\n        rofi_menu.TouchpadItem(),\n        rofi_menu.NestedMenu("Projects >", ProjectsMenu()),\n        rofi_menu.ShellItem(\n            "Downloads (show size)", "du -csh ~/Downloads", show_output=True\n        ),\n        rofi_menu.NestedMenu("Second monitor", rofi_menu.SecondMonitorMenu()),\n        rofi_menu.ShellItem("Lock screen", "i3lock -i ~/.config/i3/bg.png"),\n        rofi_menu.ShellItem("Sleep", "systemctl suspend"),\n        rofi_menu.NestedMenu("Logout", LogoutMenu()),\n    ]\n\n\nif __name__ == "__main__":\n    rofi_menu.run(MainMenu())\n```\n\nRun it as:\n\n```sh\n$ rofi -modi mymenu:/path/to/example.py -show mymenu\n```\n\nIt\'ll result in\n\n![rofi menu](https://github.com/miphreal/python-rofi-menu/raw/master/docs/menu-example.png)',
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miphreal/python-rofi-menu',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
