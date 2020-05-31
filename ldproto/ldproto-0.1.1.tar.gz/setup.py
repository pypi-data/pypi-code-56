# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ldproto']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ldproto',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Length-Delimited Proto\n\nWhen protobuf messages are either across the wire, or put in intermediary storage, it is helpful to be able to read and write individual messages in a streaming format.\n\nThis package exposes two methods:\n\n* `write_ld(writer, protomsg)` - writes one instance of a protobuf message to the stream\n* `read_ld(reader, msgtype) -> protomsg` - reads one protobuf message from the stream, using the type as the constructor\n\nThis package uses an unsigned 32-bit integer as the length-prefix.\n\n## Example\n\nAssuming there is a protobuf message with the type name "User"\n\n```python\nfrom ldproto import read_ld, write_ld\nimport myproto as pb\n\n# .ld is for length-delimited\nwith open(\'out.user.ld\', \'wb\') as f:\n    for user in users:\n        write_ld(f, user)\n\nparsed_users = []\nwith open(\'out.user.ld\', \'rb\') as f:\n    while True:\n        # Replace pb.User here with the protobuf\n        user = read_ld(f, pb.User)\n        if user is None:\n            print(\'done reading messages\')\n            break\n        parsed_users.append(user)\n```\n\nTo write to / from a bytestream in-memory, use BytesIO in-place of the files in the example.\n',
    'author': 'Sebastian Nyberg',
    'author_email': 'seb.nyberg90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
