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
    'version': '1.0.2',
    'description': 'A monkey-patch library to provide more compact representation for Stripe objects',
    'long_description': "# Stripe Repr\n\nA monkey-patch library to provide more compact representation for Stripe objects.\n\nIf you ever tried to explore the Stripe API from the console, you did notice that the representation format of the objects is overly verbose. A single call of something like `stripe.Customer.list()` pollutes the output with hundreds of lines of the output.\n\nTo simplify the exploratory work for ourselves, we created a simple `stripe_repr` library that we install in our development environment. Then we use it as-is:\n\n```python\nimport stripe_repr\n\nstripe_repr.patch()\n```\n\nThe output becomes more manageable:\n\n```\n>>> stripe.Customer.list()\nListObject(data=[Customer(id='cus_HOQHEicZ9WvOJk'), ..., Customer(id='cus_HOG3cB0b8sin1q')])\n```\n\nThe second annoyance is date-times, represented in seconds since epoch. Whenever possible, the repr tries to convert them to a proper datetime and format as a string. When it's not enough, you can call a method `formatted_dict()` that also has a shortcut `d()`.\n\n```python\nIn  [1]: stripe.Invoice.retrieve('in_xxxxx).d()\nOut [1]:\n {'id': 'in_xxxxx',\n 'object': 'invoice',\n 'account_country': 'US',\n ...\n 'created': '2020-06-02T16:58:18',\n 'currency': 'usd',\n}\n```\n",
    'author': 'Doist Developers',
    'author_email': 'dev@doist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Doist/stripe-repr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0',
}


setup(**setup_kwargs)
