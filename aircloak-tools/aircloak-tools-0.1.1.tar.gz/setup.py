# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aircloak_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.4,<2.0.0', 'psycopg2>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'aircloak-tools',
    'version': '0.1.1',
    'description': 'Tools for querying an Aircloak service via its postgres api.',
    'long_description': '# Python Aircloak Tools\n\nA small package for querying an Aircloak service via the postgres api. \n\nThe main aim is to provide an Aircloak-friendly wrapper around `psycopg2`, and in particular to\nprovide clear error messages when something doesn\'t go as planned. \n\nQuery results are return as `pandas` dataframes. \n\n\n## Example\n\nThe following code shows how to initiate a connection and execute a query.\n\nAs a pre-requisite you should have a username and password for the postgres interface of an\nAircloak installation (ask your admin for these). Assign these values to `AIRCLOAK_PG_USER`\nand `AIRCLOAK_PG_PASSWORD` environment variables. \n\n> Note the call to ``ac.connect()`` can be used as a context manager: Using the ``with`` statement, the connection \n> is automatically closed cleanly when it it goes out of scope.\n\n```python\nimport aircloak_tools as ac\n\nAIRCLOAK_PG_HOST = "covid-db.aircloak.com"\nAIRCLOAK_PG_PORT = 9432\n\nAIRCLOAK_PG_USER = environ.get("AIRCLOAK_PG_USER")\nAIRCLOAK_PG_PASSWORD = environ.get("AIRCLOAK_PG_PASSWORD")\n\nTEST_DATASET = "cov_clear"\n\nwith ac.connect(host=AIRCLOAK_PG_HOST, port=AIRCLOAK_PG_PORT,\n                user=AIRCLOAK_PG_USER, password=AIRCLOAK_PG_PASSWORD, dataset=TEST_DATASET) as conn:\n\n    assert(conn.is_connected())\n\n    tables = conn.get_tables()\n\n    print(tables)\n\n    feeling_now_counts = conn.query(\'\'\'\n    select feeling_now, count(*), count_noise(*)\n    from survey\n    group by 1\n    order by 1 desc\n    \'\'\')\n```\n',
    'author': 'dlennon',
    'author_email': '3168260+dandanlen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
