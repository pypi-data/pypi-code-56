# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tracker']
install_requires = \
['click>=7.1.2,<8.0.0', 'redis>=3.5.3,<4.0.0']

entry_points = \
{'console_scripts': ['redis-tracker = tracker:main']}

setup_kwargs = {
    'name': 'redis-tracker',
    'version': '1.1',
    'description': 'simple redis key tracker for stdout and prometheus',
    'long_description': '# redis-tracker\n\nCli tool that redirect redis key values to stdout and/or [prometheus](http://prometheus.io)\n\n    $ redis-tracker set zset text list --prometheus 9090\n    sending stats to prometheus: localhost:9090\n    set                                                       84\n    list                                                      57\n    zset                                                      19\n    text                                                  hello!\n\n## Prometheus\n\nThe example above would produce these prometheus stats:\n\n    # HELP redis_track redis key value tracking\n    # TYPE redis_track gauge\n    redis_track{key="set",source="redis@localhost/0:6379",type="set"} 1.0\n    redis_track{key="zset",source="redis@localhost/0:6379",type="zset"} 1.0\n    # HELP redis_track_info redis key value tracking\n    # TYPE redis_track_info gauge\n    redis_track_info{key="text",source="redis@localhost/0:6379",text="hello!",type="string"} 1.0\n    \nIn other words:\n    \n* `sets` and `lists` produce gauges that track their length\n* `zsets` same as sets\n* `string` produces `info`\n\n## Usage\n\n    $ redis-tracker --help                                                                                               \n    Usage: redis-tracker [OPTIONS] [KEYS]...\n\n      track redis keys to stdout and/or prometheus\n\n    Options:\n      --from-set TEXT       take keys from set key\n      --prometheus INTEGER  enable prometheus polling on port\n      --tick-rate INTEGER   how often to check in seconds  [default: 1]\n      --no-color            disable output color\n      -h TEXT               redis hoststring  [default: localhost]\n      -p INTEGER            redis port  [default: 6379]\n      -a TEXT               redis password\n      -db INTEGER           redis host  [default: 0]\n      --help                Show this message and exit.\n\n## Install\n\n    pip install redis-tracker\n',
    'author': 'bernardas ališauskas',
    'author_email': 'bernardas.alisauskas@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
