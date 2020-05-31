# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['locasticsearch', 'locasticsearch.client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'locasticsearch',
    'version': '0.0.1',
    'description': 'Serverless full text search in Python',
    'long_description': '# Locasticsearch\n\n<p align="center">\n    <em>Serverless full text search in Python</em>\n</p>\n\nLocasticsearch provides serverless full text search powered by [sqlite full text search capabilities](https://www.sqlite.org/fts5.html) but trying to be compatible with a subset of the elasticsearch API.\n\nThat way you can comfortably develop your text search appplication without needing to set up servers, but knowing that you are not locked in to a library. When you are ready to .\n\nThat said, if you are only doing basic search operations within the subset supported by this library, and you dont have a lot of documents (less than a million) that would justify going for a cluster deployment, Locasticsearch [can be a faster](benchmarks) alternative to Elasticsearch.\n\n<p align="center">\n<a href="https://github.com/elyase/locasticsearch/actions?query=workflow%3ATest" target="_blank">\n    <img src="https://github.com/elyase/locasticsearch/workflows/Test/badge.svg" alt="Test">\n</a>\n<a href="https://github.com/elyase/locasticsearch/actions?query=workflow%3APublish" target="_blank">\n    <img src="https://github.com/elyase/locasticsearch/workflows/Publish/badge.svg" alt="Publish">\n</a>\n<a href="https://codecov.io/gh/elyase/locasticsearch" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/elyase/locasticsearch?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/locasticsearch" target="_blank">\n    <img src="https://img.shields.io/pypi/v/locasticsearch?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/locasticsearch/" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/locasticsearch.svg" alt="Python Versions">\n</a>\n\n## Getting started\n```\nfrom locasticsearch import Locasticsearch\nfrom datetime import datetime\n\nes = Locasticsearch()\n\ndoc = {\n    "author": "kimchy",\n    "text": "Elasticsearch: cool. bonsai cool.",\n    "timestamp": datetime(2010, 10, 10, 10, 10, 10),\n}\nres = es.index(index="test-index", doc_type="tweet", id=1, body=doc)\n\nres = es.get(index="test-index", doc_type="tweet", id=1)\nprint(res["_source"])\n\nes.indices.refresh(index="test-index")\n\nres = es.search(index="test-index", body={"query": {"match_all": {}}})\nprint("Got %d Hits:" % res["hits"]["total"]["value"])\nfor hit in res["hits"]["hits"]:\n    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])\n```    \n\n## Features\n\n- 💯% local, no server management\n- ✨ Lightweight pure python, no external dependencies\n- ⚡ Super fast searches thanks to [sqlite full text search capabilities](https://www.sqlite.org/fts5.html)\n- 🔗 No lock in. Thanks to the API compatiblity with the official client, you can smoothly transition to Elasticsearch for scale or more features without changing your code.\n\n## Install\n\n```bash\npip install locasticsearch\n```\n\n## To use or not to use\n\nYou should NOT use Locasticsearch if:\n\n- you are deploying a security sensitive application. Locasticsearch code is very prone to SQL injection attacks.\n- Your searches are more complicated than what you would find in a 5 min Elasticsearch tutorial. Elasticsearch has a huge API and it is very unlikely that we can support even a sizable portion of that.\n- You hate buggy libraries. Locasticsearch is a very young project so bugs are guaranteed. Check the tests to see if your needs are covered. \n\nYou should use Locasticsearch if:\n\n- you dont want a docker or an elasticsearch service using precious resources in your laptop\n- you have basic text search needs and Elasticsearch would be overkill\n- you want very easy deployments that only involve pip installs\n- using Java from a python program makes you feel dirty \n\n\n',
    'author': 'Yaser Martinez',
    'author_email': 'yaser.martinez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
