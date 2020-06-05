# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snow',
 'snow.model',
 'snow.model.schema',
 'snow.model.schema.fields',
 'snow.model.schema.helpers',
 'snow.models',
 'snow.models.table',
 'snow.query',
 'snow.request',
 'snow.request.helpers',
 'snow.request.response',
 'snow.schemas',
 'snow.schemas.table']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'marshmallow>=3.6.1,<4.0.0']

setup_kwargs = {
    'name': 'snow',
    'version': '0.3.1',
    'description': 'Python asyncio library for ServiceNow',
    'long_description': '# snow: Python asyncio library for ServiceNow\n\n[![image](https://badgen.net/pypi/v/snow)](https://pypi.org/project/snow)\n[![image](https://badgen.net/badge/python/3.7+?color=purple)](https://pypi.org/project/snow)\n[![image](https://badgen.net/travis/rbw/snow)](https://travis-ci.org/rbw/snow)\n[![image](https://badgen.net/pypi/license/snow)](https://raw.githubusercontent.com/rbw/snow/master/LICENSE)\n[![image](https://pepy.tech/badge/snow/month)](https://pepy.tech/project/snow)\n\n\nSnow is a simple and lightweight yet powerful and extensible library for interacting with ServiceNow. It works\nwith modern versions of Python, utilizes [asyncio](https://docs.python.org/3/library/asyncio.html) and\ncan be used for simple scripting as well as for building high-concurrency backend applications on top of the ServiceNow platform.\nAlso, its API is fully type annotated and documented.\n\n*Example code*\n```python\n\nimport asyncio\n\nfrom snow import Snow\nfrom snow.schemas.table import IncidentSchema as Incident\n\napp = Snow("<instance>.service-now.com", basic_auth=("<username>", "<password>"))\n\nasync def main():\n    # Make a TableModel object from the built-in Incident schema\n    async with app.get_table(Incident) as inc:\n        # Get high-priority incidents\n        for response in await inc.get(Incident.priority <= 3, limit=5):\n            print(f"Number: {response[\'number\']}, Priority: {response[\'priority\'].text}")\n\nasyncio.run(main())\n\n```\n\nCheck out the [examples directory](examples) for more examples.\n\nDocumentation\n---\n\nThe Snow API reference and more is available in the [documentation](https://python-snow.readthedocs.io/en/latest).\n\n\nFunding\n-------\n\nThe Snow code is permissively licensed, and can be incorporated into any type of application–commercial or otherwise–without costs or limitations.\nIts author believes it\'s in the commercial best-interest for users of the project to invest in its ongoing development.\n\nConsider leaving a [donation](https://paypal.vault13.org) if you like this software, it will:\n\n- Directly contribute to faster releases, more features, and higher quality software.\n- Allow more time to be invested in documentation, issue triage, and community support.\n- Safeguard the future development of Snow.\n\nDevelopment status\n---\n\nThe fundamental components (models, client code, error handling, documentation, etc) of the library is considered complete.\nHowever, automatic testing and real-world use is somewhat lacking, i.e. there are most likely bugs lurking about,\nand the software should be considered Alpha, shortly Beta.\n\nContributing\n---\n\nCheck out the [contributing guidelines](CONTRIBUTING.md) if you want to help out with code or documentation.\n\n\nAuthor\n------\n\nRobert Wikman \\<rbw@vault13.org\\>\n\n',
    'author': 'Robert Wikman',
    'author_email': 'rbw@vault13.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rbw/snow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
