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
    'version': '0.1.152',
    'description': 'Programming module for wave front data processing',
    'long_description': '```python\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nfrom wfslib.geometry import Geometry\nfrom wfslib.wfs import WFSData\n```\n\n### Крупная сетка засвеченная полностью \n\n\n```python\nfrom PIL import Image\n\n\npath = "../data/bad_img3.tiff"\n\narr = np.array(Image.open(path))[500:1500, 500:1500]\narr = np.expand_dims(arr, 0)\nwfs = WFSData(arr)\nwfs.geometry.set_options(shift=(-22, -36))\nwfs.reference = 27\nwfs.good_only = True #отображать только качественные субапертуры\nplt.imshow(arr[0])\nwfs.show_geometry()\n```\n\n\n\n![png](output_2_2.png)\n\n\n\n![png](output_2_3.png)\n\n\n\n```python\n#print(str (wfs[0].get_offset(43)))\nwfs.mask = True\nplt.subplot(1,2,1)\nplt.imshow(wfs[0][17])\nplt.subplot(1,2,2)\nplt.imshow(wfs[0][1])\n```\n\n\n\n\n    <matplotlib.image.AxesImage at 0x2781c39aa90>\n\n\n\n\n![png](output_3_1.png)\n\n\n### Крупная сетка хасвеченная диагонально\n\n\n```python\npath = "../data/bad_img1.tiff"\n\nGeometry.only_wavelets = 0\n\narr = np.array(Image.open(path))[500:1500, 500:1500]\narr = np.expand_dims(arr, 0)\nwfs = WFSData(arr)\nwfs.geometry.set_options(shift=(-65, -15))\nwfs.reference = 27\n\n\n\nplt.imshow(arr[0])\nwfs.show_geometry(show_type = "offsets")\n```\n\n\n\n![png](output_5_2.png)\n\n\n\n![png](output_5_3.png)\n\n\n### Мелкая сетка полностью засвеченная\n\n\n```python\nwfs = WFSData(\'../data/file.h5\', dataset_name = "data")\n#wfs.close_stream()\np = wfs.geometry.options\nprint(p)\nwfs.geometry.set_options( shift = (-1,1), border = 6)\nwfs.reference = 87\n#wfs.domask = True\n\nwfs.show_geometry()\nwfs[0].offsets()\n\n#    plt.imshow(wfs[0][172])    \nprint(wfs[1].get_offset(130))\n\n```\n\n\n    {\'border\': 8.0, \'cell_width\': 32.0, \'start_point\': [139, 99]}\n    \n\n![png](output_7_2.png)\n\n\n    [0. 0.]\n    \n\n### Точки\n\n\n```python\n\n\npath = "../data/bad_img2.tiff"\n\narr = np.array(Image.open(path))\narr = np.expand_dims(arr, 0)\n\nplt.imshow(arr[0])\nwfs = WFSData(arr)\nwfs.geometry.set_options(shift=(64, -38),swap = True, rotate = 1)\n\n#plt.imshow(arr[0])\nwfs.show_geometry()\n```\n\n    134.0\n    210.5\n    \n\n\n![png](output_9_2.png)\n\n\n\n![png](output_9_3.png)\n\n\n## Bims\n\n\n```python\ndef read_bim(path):\n    with open(path, "rb") as f:\n        ny = int.from_bytes(f.read(4), "little")\n        nx = int.from_bytes(f.read(4), "little")\n        return np.frombuffer(f.read()).reshape(ny, nx)\n```\n\n\n```python\nbim_img = read_bim("../data/bims/lsvt-z2=-2.bim").copy()\nplt.imshow(bim_img)\n```\n\n\n\n\n    <matplotlib.image.AxesImage at 0x2781c113b70>\n\n\n\n\n![png](output_12_1.png)\n\n\n\n```python\nGeometry.only_wavelets = 0\nwfs = WFSData(bim_img)\n\np = wfs.geometry.options\nprint(p)\nwfs.geometry.set_options(shift=(-56, -38))\n\nwfs.good_only = True\nwfs.reference = 0\n#plt.imshow(arr[0])\nwfs.show_geometry(show_type = "offsets")\nwfs.show_geometry()\n```\n\n\n    {\'border\': 4.0, \'cell_width\': 76.0, \'start_point\': [185, 167]}\n    \n\n![png](output_13_2.png)\n\n\n\n![png](output_13_3.png)\n\n\n### Разные функции качества\n\n\n```python\ndef qualitative_sub_std(cell, std, mean_val):\n        return np.mean(cell) > std\n    \ndef qualitative_sub_mean(cell, std, mean_val):\n        return np.mean(cell) > mean_val\n\ndef qualitative_sub_median(cell, std, mean_val):\n    return np.median(cell) > mean_val\n```\n\n\n```python\n\npath = "../data/bad_img3.tiff"\n\narr = np.array(Image.open(path))[500:1500, 500:1500]\narr = np.expand_dims(arr, 0)\nwfs = WFSData(arr)\nwfs.geometry.set_options(shift=(-22, -36))\nwfs.qualitative_function = qualitative_sub_mean\nwfs.reference = 27\n\nwfs.show_geometry()\n```\n\n    240.66666666666666\n    317.0\n    \n\n![png](output_16_2.png)\n\n\n\n```python\nwfs.qualitative_function = qualitative_sub_median\nwfs.show_geometry()\n```\n\n\n![png](output_17_0.png)\n\n\n\n```python\nwfs.qualitative_function = qualitative_sub_std\nwfs.show_geometry()\n```\n\n\n![png](output_18_0.png)\n\n\n### Cмотрим смещения\n\n\n```python\n\npath = "../data/bad_img3.tiff"\n\narr = np.array(Image.open(path))[500:1500, 500:1500]\narr = np.expand_dims(arr, 0)\nwfs = WFSData(arr)\nwfs.geometry.set_options(shift=(-22, -36))\nwfs.qualitative_function = qualitative_sub_mean\nwfs.reference = 13\nwfs.good_only = True\n\nwfs.show_geometry()\n```\n\n![png](https://sun4-15.userapi.com/4JUbKL7hF546WTnhmzGiypzLYv_47aXZWK0nXw/uzrfl3ucbEk.jpg)\n\n\n\n```python\nwfs[0].offsets()\n```\n\n\n\n\n    array([[-28., -23.],\n           [-25.,  -0.],\n           [-30.,  -0.],\n           [-29.,  -1.],\n           [-28., -43.],\n           [-25., -47.],\n           [-28.,  -0.],\n           [  1.,  -0.],\n           [ 45.,  -0.],\n           [-30., -43.],\n           [-25., -37.],\n           [ -0.,  -0.],\n           [ 24.,  -0.],\n           [ -0.,  -0.],\n           [-26.,  -1.],\n           [ 46., -35.],\n           [ 38.,  -0.],\n           [ 42.,  -0.],\n           [-30.,  -0.],\n           [ 41., -31.],\n           [ 34., -40.],\n           [ 31.,  -0.],\n           [ 41.,  -0.],\n           [ 37., -36.],\n           [ 34., -39.],\n           [ 29., -45.],\n           [ 24., -32.]])\n\n\n\n\n\n',
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
