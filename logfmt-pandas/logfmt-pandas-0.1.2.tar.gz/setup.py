# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['logfmt_pandas']

package_data = \
{'': ['*']}

install_requires = \
['logfmt>=0.4,<0.5', 'pandas>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'logfmt-pandas',
    'version': '0.1.2',
    'description': 'Read logfmt files into pandas dataframes.',
    'long_description': '# logfmt-pandas\n\nThis package reads [logfmt](https://www.brandur.org/logfmt) files as [pandas](https://pandas.pydata.org/) DataFrames.\n\n## Usage\n\n```python\nfrom io import StringIO\n\nfrom logfmt_pandas import read_logfmt\n\ndata = StringIO("x=0 y=1\\nx=1 y=2")\ndata_frame = read_logfmt(data)\n```\n\n## Testing\n\nRun\n```\npoetry run pytest\n```\n\n## Coverage\n\nRun\n```\npoetry run pytest --cov\npoetry run coverage html\n```\n\nCoverage report is written to `htmlcov/index.html`.\n',
    'author': 'Alexander Krotov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/link2xt/logfmt-pandas',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
