# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras_fsl',
 'keras_fsl.callbacks',
 'keras_fsl.dataframe',
 'keras_fsl.dataframe.operators',
 'keras_fsl.imgaug.sequentials',
 'keras_fsl.layers',
 'keras_fsl.layers.tests',
 'keras_fsl.losses',
 'keras_fsl.losses.tests',
 'keras_fsl.metrics',
 'keras_fsl.metrics.tests',
 'keras_fsl.models',
 'keras_fsl.models.encoders',
 'keras_fsl.models.head_models',
 'keras_fsl.models.head_models.tests',
 'keras_fsl.sequences',
 'keras_fsl.sequences.prediction',
 'keras_fsl.sequences.prediction.pairs',
 'keras_fsl.sequences.prediction.single',
 'keras_fsl.sequences.training',
 'keras_fsl.sequences.training.pairs',
 'keras_fsl.sequences.training.single',
 'keras_fsl.utils',
 'keras_fsl.utils.tests']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow-datasets>=3.1.0,<4.0.0',
 'tensorflow>=2.1.0,<3.0.0',
 'tqdm>=4.42.0,<5.0.0']

setup_kwargs = {
    'name': 'keras-fsl',
    'version': '0.2.0',
    'description': 'Model builders for some State-of-the-Art architectures in few-shot and contrastive learning',
    'long_description': None,
    'author': 'Clément Walter',
    'author_email': 'clement0walter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
