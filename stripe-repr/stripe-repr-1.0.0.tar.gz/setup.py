# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stripe_repr']

package_data = \
{'': ['*']}

install_requires = \
['stripe>=2.48.0,<3.0.0']

setup_kwargs = {
    'name': 'stripe-repr',
    'version': '1.0.0',
    'description': 'A monkey-patch library to provide more compact representation for Stripe objects',
    'long_description': '# Stripe Repr\n\nA monkey-patch library to provide more compact representation for Stripe objects\n\n## Getting Started\n\nUse it as this:\n\n```python\nimport stripe_repr\n\nstripe_repr.patch()\n```\n',
    'author': 'Doist Developers',
    'author_email': 'dev@doist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Doist/stripe-repr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
