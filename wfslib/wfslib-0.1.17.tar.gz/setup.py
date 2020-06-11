# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wfslib']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['wfslib = entry:main']}

setup_kwargs = {
    'name': 'wfslib',
    'version': '0.1.17',
    'description': 'Programming module for wave front data processing',
    'long_description': "**wfslib** is open library for wave front data processing: \n\n* different data type usage (hfd, bim, numpy);\n* automatic geometry calculation;\n* offsets calculation;\n* settings-tools for manage yours data.\n\n### Example of wfslib work\n\n\n```python\nfrom wfslib.wfs import WFSData\n\nwfs = WFSData('../data/subpixel_test.h5', dataset_name = 'wfss/n0/detector') #Load data\n\np = wfs.geometry.options #Geometry options\nprint(p)\nwfs.reference = 8\n\n#Change geometry options\nwfs.geometry.set_options(shift=(-p['start_point'][0]+1,-p['start_point'][1]+1), border = 0, cell_width = p['cell_width']-1)\n#Visualization\nwfs.show_geometry()\n```\n\n\n\n    {'border': 4.0, 'cell_width': 110.0, 'start_point': [168, 131]}\n    \n\n\n![jpg](https://sun4-12.userapi.com/G3ulaQxVXOs1Wubv6BmAOLaFN2l-v0IVHuaAaw/Xu-2xvIdMVY.jpg)\n\n\n\n```python\nwfs[0].offsets()[:5] #Calculate offsets\n```\n\n\n\n\n\n    array([[-0., -0.],\n           [-0., -0.],\n           [-1., -1.],\n           [-1.,  1.],\n           [22.,  9.]])\n\n\n\n\n```python\n\n```\n\n\n```python\n\n```\n\n\n```python\n\n```\n",
    'author': 'Zoya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
