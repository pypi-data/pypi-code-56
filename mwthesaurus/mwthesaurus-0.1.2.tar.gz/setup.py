# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mwthesaurus']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'mwthesaurus',
    'version': '0.1.2',
    'description': 'API Wrapper for the Merriam-Webster Collegiate Thesaurus API.',
    'long_description': '# mwthesaurus\n\nSmall wrapper around the Merriam-Webster API. Has both a sync and async interface thanks to [httpx](https://github.com/encode/httpx).\n\n## Installation\n\n`pip install mwthesaurus`\n\n## Usage\n\nBasic usage:\n\n```python\n>>> from mwthesaurus import MWClient\n>>> client = MWClient(key="YOUR-KEY-HERE")\n>>> client.get("python")\n[Word(word=\'python\', wordtype=\'noun\', shortdef=[\'as in anaconda, boa\'], synonyms=[\'adder\', \'anaconda\', \'asp\', \'black racer\', \'blacksnake\', \'blue racer\', \'boa\', \'bull snake\', \'bushmaster\', \'chicken snake\', \'cobra\', \'constrictor\', \'copperhead\', \'coral snake\', \'cottonmouth moccasin\', \'diamondback rattlesnake\', \'fer-de-lance\', \'garter snake\', \'gopher snake\', \'green snake\', \'hognose snake\', \'horned viper\', \'indigo snake\', \'king cobra\', \'king snake\', \'krait\', \'mamba\', \'milk snake\', \'moccasin\', \'pine snake\', \'pit viper\', \'puff adder\', \'racer\', \'rat snake\', \'rattlesnake\', \'sea serpent\', \'sea snake\', \'sidewinder\', \'taipan\', \'water moccasin\', \'water snake\', \'worm snake\', \'serpent\', \'snake\', \'viper\'], antonyms=[], stems=[\'python\'])]\n...\n>>> import asyncio\n>>> asyncio.run(client.aget("python"))\n[Word(word=\'python\', wordtype=\'noun\', shortdef=[\'as in anaconda, boa\'], synonyms=[\'adder\', \'anaconda\', \'asp\', \'black racer\', \'blacksnake\', \'blue racer\', \'boa\', \'bull snake\', \'bushmaster\', \'chicken snake\', \'cobra\', \'constrictor\', \'copperhead\', \'coral snake\', \'cottonmouth moccasin\', \'diamondback rattlesnake\', \'fer-de-lance\', \'garter snake\', \'gopher snake\', \'green snake\', \'hognose snake\', \'horned viper\', \'indigo snake\', \'king cobra\', \'king snake\', \'krait\', \'mamba\', \'milk snake\', \'moccasin\', \'pine snake\', \'pit viper\', \'puff adder\', \'racer\', \'rat snake\', \'rattlesnake\', \'sea serpent\', \'sea snake\', \'sidewinder\', \'taipan\', \'water moccasin\', \'water snake\', \'worm snake\', \'serpent\', \'snake\', \'viper\'], antonyms=[], stems=[\'python\'])]\n```\n\n`MWClient.get()` returns a list of definitions for a given word.\n\nIf you want the definitions as dictionaries, just pass the results to `dataclasses.asdict()`:\n\n```python\n>>> from dataclasses import asdict\n>>> [asdict(w) for w in client.get("python")]  \n[{\'word\': \'python\', \'wordtype\': \'noun\', \'shortdef\': [\'as in anaconda, boa\'], \'synonyms\': [\'adder\', \'anaconda\', \'asp\', \'black racer\', \'blacksnake\', \'blue racer\', \'boa\', \'bull snake\', \'bushmaster\', \'chicken snake\', \'cobra\', \'constrictor\', \'copperhead\', \'coral snake\', \'cottonmouth moccasin\', \'diamondback rattlesnake\', \'fer-de-lance\', \'garter snake\', \'gopher snake\', \'green snake\', \'hognose snake\', \'horned viper\', \'indigo snake\', \'king cobra\', \'king snake\', \'krait\', \'mamba\', \'milk snake\', \'moccasin\', \'pine snake\', \'pit viper\', \'puff adder\', \'racer\', \'rat snake\', \'rattlesnake\', \'sea serpent\', \'sea snake\', \'sidewinder\', \'taipan\', \'water moccasin\', \'water snake\', \'worm snake\', \'serpent\', \'snake\', \'viper\'], \'antonyms\': [], \'stems\': [\'python\']}]\n```\n',
    'author': 'Peder Hovdan Andresen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PederHA/mwthesaurus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
