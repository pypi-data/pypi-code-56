# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squaternion']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

setup_kwargs = {
    'name': 'squaternion',
    'version': '0.3.1',
    'description': 'Some simple functions for quaternion math',
    'long_description': '![](https://images.pexels.com/photos/45246/green-tree-python-python-tree-python-green-45246.jpeg?cs=srgb&dl=green-snake-45246.jpg&fm=jpg)\n\n# Simple Quaternions (`squaternion`)\n\n[![Actions Status](https://github.com/MomsFriendlyRobotCompany/squaternion/workflows/CheckPackage/badge.svg)](https://github.com/MomsFriendlyRobotCompany/squaternion/actions)\n![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/squaternion)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/squaternion)\n![PyPI](https://img.shields.io/pypi/v/squaternion)\n\nGenerally I don\'t need all of the capabilities (or complexity) of `quaternion`\nmath libraries. Basically I just need a way to convert between Euler and\nQuaternion representations and have a nice way to print them out.\n\nThis has basically no imports outside of standard python 3.x libraries.\nIt should be easier to get on embedded python systems without having to build\n`numpy`. Also, this tries to be *fast* by using a frozen class with slots and\nwhere it makes sense, returns `tuples` instead of `list`s.\n\n### Alternatives\n\nThis is a basic library that converts between Euler angles and Quaternions.\nThere are other libraries that do so much more listed below ... but I don\'t\nneed all of that.\n\n- [scipy.spatial.transform.Rotation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html#scipy.spatial.transform.Rotation): has everything you could want, with lots of imports\n- [tinyquaternion](https://github.com/rezaahmadzadeh/tinyquaternion): appears to be more functional but needs `numpy`\n- [quaternions](https://github.com/mjsobrep/quaternions): another good lightweight quaternion package\n\n## Install\n\n```\npip install squaternion\n```\n\n## Usage\n\n```python\nfrom squaternion import Quaternion\n\n# if you know the values you want Quaternion(w, x, y, z), note this is a\n# attr frozen class so it is immutable once created\nq = Quaternion(1,0,0,0)\n\n# however you typically don\'t think in 4 dimensions, so create from\n# euler angles from_eluer(roll, pitch, yaw), default is radians, but set\n# degrees true if giving degrees\nq = Quaternion.from_euler(0, -90, 100, degrees=True)\n\n# can get the euler angles back out in degrees (set to True)\ne = q.to_euler(degrees=True)\nd = q.to_dict()\n\n# iterate through values\nfor i in q:\n    print(f"{i}")\n\n# indexing like a namedtuple\nz = q[3]\nz = q[-1]\nv = q[-3:]\nw = q[0]\n\n# class properties\nv = q.vector     # returns a tuple (x,y,z)\ns = q.scalar     # returns a double (w)\nn = q.normalize  # returns unit quaternion\nm = q.magnitude  # returns the magnitude of the quaternion\na = q.angle      # returns angle of rotation in radians\na = q.axis       # returns axis of rotation\n\n# useful attr functions\nq == q    # compare will return True\nq != q    # will return False\nprint(q)  # pretty print\nw = q.w\nx = q.x\ny = q.y\nz = q.z\n```\n\n## References\n\n- [Wikipedia Convert Between Quaternions and Euler Angles](https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles)\n- [Wikipedia Euler Angle Definitions](https://en.wikipedia.org/wiki/Euler_angles#Conventions_2)\n- [Wikipedia Gimbal Lock](https://en.wikipedia.org/wiki/Gimbal_lock)\n\n# MIT License\n\nCopyright (c) 2018 Kevin Walchko\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/squaternion/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
