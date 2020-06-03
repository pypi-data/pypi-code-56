# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['defaultenv']
setup_kwargs = {
    'name': 'defaultenv',
    'version': '0.0.13',
    'description': 'Environment and .env file reader',
    'long_description': '# defaultenv\n\nEnvironment and config file reader for python3.\n**Warrning:** slightly magic inside. This module magically read and use environment value both from \'.env\' file and environment itself.\n\n*Since version 0.0.6 `.env` file will be rereaded on the fly on next `env` call, so now your environment is always up to date.*\n\n```python\n$ echo "MY_VAL=\'test\'" > .env\n$ python\n>>> from defaultenv import env\n>>> env(\'PATH\')\n\'/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin\'\n>>> env(\'TEST\')\n>>> env(\'MY_VAL\')\n\'test\'\n>>> import os; os.environ[\'MY_VAL\']\n\'test\'\n\n```\n\n`env` method may be used to check the value of variable.\nIf variable is not defined `env` method will return `None`.\nIf both environment variable and corresponding .env record is exist then  .env have a priority.\nAnd yes, you can use `os.environ` instead of  `env()`, all records from .env will be exported immidiately.\n\nFor additional convinience you can use `env()` with `default` argument, for example:\n\n```python\n>>> from defaultenv import env\n>>> env(\'TEST\', \'no test\')\n\'no test\'\n>>> env(\'UID\')\n\'1000\'\n>>> env(\'UID\', int)\n1000\n>>> env(\'HOME\', pathlib.Path)\nPosixPath("/home/bobuk")\n>>> env(\'PATH\', lambda x: [pathlib.Path(_) for _ in x.split(\':\')])\n[PosixPath(\'/usr/local/sbin\'), PosixPath(\'/usr/local/bin\'), PosixPath(\'/usr/sbin\'), PosixPath(\'/usr/bin\'),\n PosixPath(\'/sbin\'), PosixPath(\'/bin\')]\n```\n\nIf `default` argument for `env()` is not empty, and key what you looking for is not exists `env()` will return you value of default.\nBut if `default` is callable (like object, lambda or function) then instead value of key from environment will be passed to this callable.\nMy favorite is to send just `int` because it\'s the easiest way to convert your default to integer.\n\nSince version 0.0.2 for more convinience two classes (ENV and ENVC) was added. You can use your environment variable name without method calling.\n\n```python\n$ python\n>>> from defaultenv import ENV\n>>> ENV.PATH\n\'/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin\'\n```\n\nENV usage removing unnesesery typing of perenthesis and quotes. In this example i\'ve save 4 keystrokes for you. But it\'s not very convinient to type uppercased name everytime. Let\'s imagine what my pinky finger is killing me.\n\n```python\n$ python\n>>> from defaultenv import ENVC as env\n>>> env.shell\n\'/usr/local/bin/zsh\'\n>>> env.home\n\'/home/bobuk\'\n```\n\nAs you can see `ENVC` convert your variable name to uppercase.\nFor both ENVC and ENV there\'s a method `defaults` to add default values of callables (as for `env` above).\n\n```python\n>>> from defaultenv import ENVC as env\n>>> env.defaults(test = 1, path = lambda x: x.split(\':\'), pid=int)\n>>> env.test\n1\n>>> env.path\n[\'/usr/local/sbin\', \'/usr/local/bin\', \'/usr/sbin\', \'/usr/bin\', \'/sbin\', \'/bin\']\n```\n\nWhat the difference between `os.environ.get(\'PATH\', None)` and `env.path`? It\'s easy to calculate and the result is 21 (which is half of 42).\n\nSince version 0.0.9 you can use even more authomated `ENVCD` which is `ENVC` but with predefined defaults.\nEvery path (or colon-separated paths list) will be defaulted to `PosixPath`, every digital value converted to `int`.\n\n```python\n>>> from defaultenv import ENVCD as env\n>>> env.path\n[PosixPath(\'/usr/local/bin\'), PosixPath(\'/usr/local/bin\'), PosixPath(\'/usr/bin\'), PosixPath(\'/bin\'), PosixPath(\'/usr/sbin\')]\n```',
    'author': 'Grigory Bakunov',
    'author_email': 'thebobuk@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/bobuk/defaultenv',
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
