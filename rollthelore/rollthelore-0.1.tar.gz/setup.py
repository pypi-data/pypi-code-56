# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loreroll']

package_data = \
{'': ['*'], 'loreroll': ['data/*']}

modules = \
['rollnpc']
install_requires = \
['click>=7.1.2,<7.2.0', 'strictyaml>=1.0.6,<1.1.0']

entry_points = \
{'console_scripts': ['rollnpc = rollnpc:generate']}

setup_kwargs = {
    'name': 'rollthelore',
    'version': '0.1',
    'description': 'An unseen servant providing an advantage to DMs/GMs while creating their worlds.',
    'long_description': "# RollTheLore\nAn *unseen servant* providing an *advantage* to DMs/GMs while creating their worlds.\n\n[![Build Status](https://travis-ci.com/geckon/rollthelore.svg?branch=master)](https://travis-ci.com/geckon/rollthelore)\n\nAs a DM, have you ever needed to lower the *DC* for the world building skill\ncheck? Did you need to create the right NPC for your players to interact with\nand thought you could use a *divine intervention*? Were you out of ideas and\nfelt like an *inspiration die* or a bit of *luck* was all that you needed? This\ntool will probably not fulfill all your *wish*es but it can at least provide\n*guidance*.\n\nRollTheLore is a tool from a DM to other DMs out there but it can also help\nplayers as it's supposed to inspire you while not only creating your world,\na shop or a random NPC encounter but it can also be used to help with your\nbackstories.\n\nAs of now it can only randomly create NPCs but I have some ideas for generating\ntowns as well and who knows? Maybe there will be even more. RollTheLore is not\nmeant to be a perfect tool but rather a simple one that still can provide very\nvaluable ideas for your campaigns and stories. At least for me personaly it\nworks very well as I often need a few simple points I can use as inspiration\nand build more fluff around it with both imagination and improvisation.\n\nSometimes the generated character doesn't make much sense but often that is\nexactly the fun part. When I need an NPC for a story I like to *roll* a few of\nthem and pick one as a basis, then I build on that. It can also be used to\npre-roll a few NPCs in advance and then use them e.g. when your playes decide\nto enter a shop or address a person you you hadn't planned beforehand.\n\nPrimarily RollTheLore is intended to be used with DnD 5e but it can very well\nserve for other game systems as well. The imagination is what matters the most.\n\nPlease note that the tool is under development. Ideas, comments and bug reports are\nwelcome!\n\n## Installation\n\n```\npip install rollthelore\n```\n\n## Usage\n\n```\n$ rollnpc.py --help\nUsage: rollnpc.py [OPTIONS]\n\n  Generate 'number' of NPCs and print them.\n\nOptions:\n  -a, --age-allowed TEXT       Allowed age(s).\n  -A, --age-disallowed TEXT    Disallowed age(s).\n  -c, --class-allowed TEXT     Allowed class(es).\n  -C, --class-disallowed TEXT  Disallowed class(es).\n  -d, --detail-level INTEGER   Amount of details generated (one or higher).\n  -n, --number INTEGER         Number of NPCs to generate.\n  -r, --race-allowed TEXT      Allowed race(s).\n  -R, --race-disallowed TEXT   Disallowed race(s).\n  --help                       Show this message and exit.\n```\n\n## Examples\n\n```\n$ rollnpc.py\nName: Zaniel\nAge: older\nRace: tabaxi\nClass: monk\nAppearance: deaf, blind\nPersonality: discouraging, disrespectful\n```\n\n```\n$ rollnpc.py -n3\nName: Iseult\nAge: old\nRace: dragonborn\nClass: fighter\nAppearance: cain, moustache\nPersonality: courteous, foolish\n\nName: Nyssa\nAge: adult\nRace: dragonborn\nClass: barbarian\nAppearance: hook instead of a hand, underbite\nPersonality: miserable, suspicious\n\nName: Briallan\nAge: older\nRace: human\nClass: wizard\nAppearance: skinny, tall\nPersonality: honorable, stylish\n```\n\n```\n$ rollnpc.py -n2 -r elf\nName: Evadne\nAge: young\nRace: elf (wood)\nClass: ranger\nAppearance: silent voice, cute\nPersonality: dependable, honorable\n\nName: Ianthe\nAge: young\nRace: half-elf\nClass: warlock\nAppearance: handlebar beard, fire-burnt skin\nPersonality: witty, organized\n```\n\n```\n$ rollnpc.py --detail-level 1\nName: Séverin\nAge: young\nRace: tiefling\nAppearance: mute\nPersonality: happy\n```\n\n```\n$ rollnpc.py --detail-level 3\nName: Korbin\nAge: adult\nRace: gnome (forest)\nClass: ranger\nAppearance: big nose, scarred, sinewy\nPersonality: grim, regretful, naive\n\n```\n",
    'author': 'Tomáš Heger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
