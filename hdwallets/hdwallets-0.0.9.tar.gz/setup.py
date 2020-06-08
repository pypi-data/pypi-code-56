# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdwallets']

package_data = \
{'': ['*']}

install_requires = \
['ecdsa>=0.14.0,<0.16.0']

setup_kwargs = {
    'name': 'hdwallets',
    'version': '0.0.9',
    'description': 'Python implementation of the BIP32 key derivation scheme',
    'long_description': '# hdwallets\n\nA basic implementation of the [bip-0032](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki).\n\nA fork of https://github.com/darosior/python-bip32 with some notable changes:\n- base58 dependency removed. All interfaces input and output raw bytes instead of base58 strings.\n- Replaced https://pypi.org/project/coincurve/ dependency with https://pypi.org/project/ecdsa/\n- Distributes type information (PEP 561)\n\n## Usage\n\n```python\n>>> from hdwallets import BIP32, HARDENED_INDEX\n>>> bip32 = BIP32.from_seed(bytes.fromhex("01"))\n# Specify the derivation path as a list ...\n>>> bip32.get_xpriv_from_path([1, HARDENED_INDEX, 9998])\n\'xprv9y4sBgCuub5x2DtbdNBDDCZ3btybk8YZZaTvzV5rmYd3PbU63XLo2QEj6cUt4JAqpF8gJiRKFUW8Vm7thPkccW2DpUvBxASycypEHxmZzts\'\n# ... Or in usual m/the/path/\n>>> bip32.get_xpriv_from_path("m/1/0\'/9998")\n\'xprv9y4sBgCuub5x2DtbdNBDDCZ3btybk8YZZaTvzV5rmYd3PbU63XLo2QEj6cUt4JAqpF8gJiRKFUW8Vm7thPkccW2DpUvBxASycypEHxmZzts\'\n>>> bip32.get_xpub_from_path([HARDENED_INDEX, 42])\n\'xpub69uEaVYoN1mZyMon8qwRP41YjYyevp3YxJ68ymBGV7qmXZ9rsbMy9kBZnLNPg3TLjKd2EnMw5BtUFQCGrTVDjQok859LowMV2SEooseLCt1\'\n# You can also use "h" or "H" to signal for hardened derivation\n>>> bip32.get_xpub_from_path("m/0h/42")\n\'xpub69uEaVYoN1mZyMon8qwRP41YjYyevp3YxJ68ymBGV7qmXZ9rsbMy9kBZnLNPg3TLjKd2EnMw5BtUFQCGrTVDjQok859LowMV2SEooseLCt1\'\n# You can use pubkey-only derivation\n>>> bip32 = BIP32.from_xpub("xpub6AKC3u8URPxDojLnFtNdEPFkNsXxHfgRhySvVfEJy9SVvQAn14XQjAoFY48mpjgutJNfA54GbYYRpR26tFEJHTHhfiiZZ2wdBBzydVp12yU")\n>>> bip32.get_xpub_from_path([42, 43])\n\'xpub6FL7T3s7GuVb4od1gvWuumhg47y6TZtf2DSr6ModQpX4UFGkQXw8oEVhJXcXJ4edmtAWCTrefD64B9RP4sYSkSumTW1wadTS3SYurBGYccT\'\n>>> bip32.get_xpub_from_path("m/42/43")\n\'xpub6FL7T3s7GuVb4od1gvWuumhg47y6TZtf2DSr6ModQpX4UFGkQXw8oEVhJXcXJ4edmtAWCTrefD64B9RP4sYSkSumTW1wadTS3SYurBGYccT\'\n>>> bip32.get_pubkey_from_path("m/1/1/1/1/1/1/1/1/1/1/1")\nb\'\\x02\\x0c\\xac\\n\\xa8\\x06\\x96C\\x8e\\x9b\\xcf\\x83]\\x0c\\rCm\\x06\\x1c\\xe9T\\xealo\\xa2\\xdf\\x195\\xebZ\\x9b\\xb8\\x9e\'\n```\n\n## Installation\n\n```\npip install hdwallets\n```\n\n## Interface\n\nAll public keys below are compressed.\n\nAll `path` below are a list of integers representing the index of the key at each depth.\n\n### BIP32\n\n#### from_seed(seed)\n\n__*classmethod*__\n\nInstanciate from a raw seed (as `bytes`). See [bip-0032\'s master key\ngeneration](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#master-key-generation).\n\n#### from_xpriv(xpriv)\n\n__*classmethod*__\n\nInstanciate with an encoded serialized extended private key (as `str`) as master.\n\n#### from_xpub(xpub)\n\n__*classmethod*__\n\nInstanciate with an encoded serialized extended public key (as `str`) as master.\n\nYou\'ll only be able to derive unhardened public keys.\n\n#### get_extended_privkey_from_path(path)\n\nReturns `(chaincode (bytes), privkey (bytes))` of the private key pointed by the path.\n\n#### get_privkey_from_path(path)\n\nReturns `privkey (bytes)`, the private key pointed by the path.\n\n#### get_extended_pubkey_from_path(path)\n\nReturns `(chaincode (bytes), pubkey (bytes))` of the public key pointed by the path.\n\nNote that you don\'t need to have provided the master private key if the path doesn\'t\ninclude an index `>= HARDENED_INDEX`.\n\n#### get_pubkey_from_path(path)\n\nReturns `pubkey (bytes)`, the public key pointed by the path.\n\nNote that you don\'t need to have provided the master private key if the path doesn\'t\ninclude an index `>= HARDENED_INDEX`.\n\n#### get_xpriv_from_path(path)\n\nReturns `xpriv (str)` the serialized and encoded extended private key pointed by the given\npath.\n\n#### get_xpub_from_path(path)\n\nReturns `xpub (str)` the serialized and encoded extended public key pointed by the given\npath.\n\nNote that you don\'t need to have provided the master private key if the path doesn\'t\ninclude an index `>= HARDENED_INDEX`.\n\n### get_master_xpriv(path)\n\nEquivalent to `get_xpriv_from_path([])`.\n\n### get_master_xpub(path)\n\nEquivalent to `get_xpub_from_path([])`.\n',
    'author': 'hukkinj1',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/hdwallets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
