# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdk_chalice_lite']

package_data = \
{'': ['*']}

install_requires = \
['aws_cdk.aws_s3_assets>=1.42.1,<2.0.0',
 'aws_cdk.core>=1.42.1,<2.0.0',
 'chalice>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'cdk-chalice-lite',
    'version': '0.1.7',
    'description': 'Utility to facilitate deploying Chalice via the cdk',
    'long_description': "# cdk-chalice-lite\n\n![](https://github.com/knowsuchagency/cdk-chalice-lite/workflows/black/badge.svg)\n![](https://github.com/knowsuchagency/cdk-chalice-lite/workflows/unit%20tests/badge.svg)\n\nLike `cdk-chalice`, but different.\n\n# Usage\n\n```python\nfrom aws_cdk import core\n\nfrom cdk_chalice_lite import Chalice\n\n\nclass MyStack(core.Stack):\n\n    def __init__(self, scope, id, chalice_app_id, directory, **kwargs):\n        super().__init__(scope, id, **kwargs)\n\n        # note, the directory parameter can be either the root directory\n        # of your chalice app i.e. where app.py is\n        # or it can be the directory of the output of `chalice package`\n\n        # if you choose the former, you can override the values in\n        # .chalice/config.json via the stage_config and lambdas_config\n        # parameters to the Chalice constructor\n\n        self.chalice = Chalice(self, chalice_app_id, directory)\n\n\n\n\napp = core.App()\n\nmy_stack = MyStack(app, 'my-stack')\n\napp.synth()\n```\n",
    'author': 'Stephan Fitzpatrick',
    'author_email': 'knowsuchagency@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/cdk-chalice-lite/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
