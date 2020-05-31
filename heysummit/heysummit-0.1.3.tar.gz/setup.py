# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heysummit']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'heysummit',
    'version': '0.1.3',
    'description': 'HeySummit API Client',
    'long_description': '=====================\nHey Summit API Client\n=====================\n\n\n.. image:: https://img.shields.io/pypi/v/heysummit.svg\n        :target: https://pypi.python.org/pypi/heysummit\n\n.. image:: https://img.shields.io/github/workflow/status/fzipi/hey-summit/CI\n        :target: https://github.com/fzipi/hey-summit/actions\n\n.. image:: https://readthedocs.org/projects/heysummit/badge/?version=latest\n        :target: https://heysummit.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n.. image:: https://pyup.io/repos/github/fzipi/hey-summit/shield.svg\n     :target: https://pyup.io/repos/github/fzipi/hey-summit/\n     :alt: Updates\n\n\n\nHey Summit API is a requests based client to the Hey Summit API.\n\n\n* Free software: Apache 2.0 License\n* Documentation: https://api-docs.heysummit.com/#introduction\n\n\nFeatures\n--------\n\nAll features from the HeySummit API are implemented. Sadly the API seems unversioned at this point so I cannot guarantee stability.\n\nExamples\n--------\n\nThe only required argument is the HeySummit API token.\n\nThis is an example usage::\n\n  import argparse\n\n  from heysummit.api import HeySummit, HeySummitException\n\n  def list_attendees():\n      attendees = hey.get_all_attendees()\n\n      print("There are {n} attendees".format(len(attendees)))\n      for attendee in attendees:\n          print("id: {id}, email: {email}".format(\n                  id=attendee[\'id\'], email=attendee[\'email\']\n                  )\n          )\n\n  def get_events():\n      events = hey.get_events(is_live=True)\n\n      for event in events:\n        print(event)\n\n  # main\n\n  # Parse Arguments\n  parser = argparse.ArgumentParser(description=\'HeySummit interaction script.\')\n  parser.add_argument(\'-t\', \'--token\', type=str, help=\'API Token. Example: jdoe.\', required=True)\n\n  args = parser.parse_args()\n\n  hey = HeySummit(token=args.token)\n\n  print(hey.get_all_attendees(event=5573))\n\n  talks = hey.get_talks(event=5573, is_active=True)\n\n  for talk in talks:\n      print(talk)\n\n\n',
    'author': 'Felipe Zipitria',
    'author_email': 'felipe.zipitria@owasp.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fzipi/hey-summit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
