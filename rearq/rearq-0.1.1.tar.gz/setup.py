# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rearq']

package_data = \
{'': ['*']}

install_requires = \
['aioredis', 'asyncclick', 'crontab', 'pydantic']

entry_points = \
{'console_scripts': ['rearq = rearq.cli:main']}

setup_kwargs = {
    'name': 'rearq',
    'version': '0.1.1',
    'description': 'Rewrite arq and make improvement.',
    'long_description': '# Rearq\n\n## Introduction\n\nRearq is a distributed task queue with asyncio and redis, which rewrite from [arq](https://github.com/samuelcolvin/arq) and make improvement.\n\n## Install\n\nJust install from pypi:\n\n```shell\n> pip install rearq\n```\nor install latest code from github:\n```shell\npip install -e git+https://github.com/long2ice/rearq.git\n```\n## Quick Start\n\n### Task Definition\n\n```python\n# main.py\nrearq = ReArq()\n\n\n@rearq.on_shutdown\nasync def on_shutdown(r):\n    print("shutdown")\n\n\n@rearq.on_startup\nasync def on_startup(r):\n    print("startup")\n\n\n@rearq.task(queue = "myqueue")\nasync def add(worker, a, b):\n    return a + b\n\n@rearq.task(cron=CronTab("*/5 * * * * * *"))\nasync def timer(worker):\n    return "timer"\n```\n\n### Run rearq worker\n\n```shell\n> rearq worker main:rearq -q myqueue\n```\n\n```log\n2020-06-04 15:37:02 - rearq.worker:92 - INFO - Start worker success with queue: myqueue\n2020-06-04 15:37:02 - rearq.worker:84 - INFO - redis_version=6.0.1 mem_usage=1.47M clients_connected=25 db_keys=5\n```\n\n### Run rearq timing worker\n\nIf you have timeing task, run another command also:\n\n```shell\n> rearq worker -t main:rearq\n```\n\n```log\n2020-06-04 15:37:44 - rearq.worker:346 - INFO - Start timer worker success with queue: myqueue\n2020-06-04 15:37:44 - rearq.worker:84 - INFO - redis_version=6.0.1 mem_usage=1.47M clients_connected=25 db_keys=5\n```\n\n## Why not arq\n\nThanks great work of `arq`, but that project is not so active now and lack of maintenance. On the other hand, I don\'t like some solution of `arq` and it\'s api, so I open this project and aims to work better.\n\n## What\'s the differences\n\n### Api\n\nRearq provide more friendly api to add register and add task, inspired by `celery`.\n\nRearq:\n\n```python\nrearq = Rearq()\n\n@rearq.task()\nasync def add(worker, a, b):\n    return a + b\n\njob = await add.delay(args=(1, 2))\nprint(job)\n```\n\nArq:\n\n```python\nclass WorkerSettings:\n    functions = [ add ]\n    redis_settings = RedisSettings(**settings.ARQ)\n\nasync def add(ctx, a,b):\n    return a + b\n\nawait arq.enqueue_job(\'add\', 1, 2)\n```\n\n### Queue implementation\n\nArq use redis `zset` to make delay queue and timing queue, and Rearq use `zset` and `stream` with `ack`.\n\n## ThanksTo\n\n- [arq](https://github.com/samuelcolvin/arq), Fast job queuing and RPC in python with asyncio and redis.\n\n## License\n\nThis project is licensed under the [MIT](https://github.com/long2ice/rearq/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/rearq.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
