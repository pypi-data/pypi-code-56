# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyncov']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1,<2.0.0']

extras_require = \
{'tqdm': ['tqdm>=4.46.0,<5.0.0']}

setup_kwargs = {
    'name': 'pyncov',
    'version': '0.1.0',
    'description': 'Pyncov-19 is a tiny probabilistic simulator for SARS-CoV-2',
    'long_description': "# Pyncov-19: Simulating the spread of SARS-CoV-2\n\nPyncov-19 is a tiny probabilistic simulator for SARS-CoV-2 implemented in Python 3, whose only dependency is Numpy 1.18.\nThis simulator is used to learn and predict the temporal dynamics of COVID-19 that are shown in https://covid19-modeling.github.io. It implements a probabilistic compartmental model at the individual level using a Markov Chain model with temporal transitions that were adjusted using the most recent scientific evidence.\n\nThis library is still a proof-of-concept and it's inteded only to be used for research and experimentation. For more information please read our [preprint](https://arxiv.org/abs/2004.13695):\n\n\n    Matabuena, M., Meijide-García, C., Rodríguez-Mier, P., & Leborán, V. (2020). \n    COVID-19: Estimating spread in Spain solving an inverse problem with a probabilistic model. \n    arXiv preprint arXiv:2004.13695. https://arxiv.org/abs/2004.13695\n\n\nThis model's main goal is to estimate the levels of infections (or the seroprevalence) of the population, using only data from the registered deaths caused by COVID-19. Although the model can be used to make future predictions (evolution of infections, fatalities, etc.), that's not the primary purpose of the model. Given the uncertainty about essential events that alter the course and dynamics of the spread (for example, the use of masks, lockdowns, social distance, etc.), it is tough to make accurate predictions, so we limit ourselves to use the model to reveal more information about what happened before (backcasting).\n",
    'author': 'Pablo R. Mier',
    'author_email': 'pablo.rodriguez-mier@inrae.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/covid19-modeling/pyncov-19',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
