# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyncov', 'pyncov.io']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1,<2.0.0']

extras_require = \
{'tqdm': ['tqdm>=4.46.0,<5.0.0']}

setup_kwargs = {
    'name': 'pyncov',
    'version': '0.1.2',
    'description': 'Pyncov-19 is a tiny probabilistic simulator for SARS-CoV-2',
    'long_description': "# Pyncov-19: Learn and predict the spread of COVID-19\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1LzTsXcisv_v_w4q6o9GxvuAzToExFGaG?usp=sharing)\n\nPyncov-19 is a tiny probabilistic simulator for SARS-CoV-2 implemented in Python 3, whose only dependency is Numpy 1.18.\nThis simulator is used to learn and predict the temporal dynamics of COVID-19 that are shown in https://covid19-modeling.github.io. It implements a probabilistic compartmental model at the individual level using a Markov Chain model with temporal transitions that were adjusted using the most recent scientific evidence.\n\n## Quick Start\n\nInstallation using pip:\n\n```bash\npip install pyncov\n```\n\nSampling 1000 simulated trajectories of the SARS-CoV-2 spread in Madrid:\n\n```python\nimport pyncov as nc\n\nsusceptible = 6680000\ninfected = 1\nnum_days = 100\n\n# Those parameters were fitted using Pyncov-19 with CMAES\nrit_params = [1.76206245, 0.73465654, 11.46818215, 0.01691976]\n# Use the default Ri(t) function with the provided parameters to calculate the daily individual dynamic reproduction rate\ndaily_ri_values = [nc.default_rit_function(i, rit_params) for i in range(num_days)]\n\n# Instantiate the model with the default parameters and sample 1,000 chains\n# NOTE: show_progress requires the TQDM library not installed by default.\nm = nc.build_markovchain(nc.MARKOV_DEFAULT_PARAMS)\nsimulations = nc.sample_chains(susceptible, infected, m, daily_ri_values, \n                               num_chains=1000, n_workers=4, show_progress=True)\n\n```\n\nA more detailed explanation can be found in the notebook included in the repository https://github.com/covid19-modeling/pyncov-19/blob/master/notebooks/basics.ipynb\n\n\n\n## About\n\nThis library is still a proof-of-concept and it's inteded only to be used for research and experimentation. For more information please read our [preprint](https://arxiv.org/abs/2004.13695):\n\n> Matabuena, M., Meijide-García, C., Rodríguez-Mier, P., & Leborán, V. (2020). \n**COVID-19: Estimating spread in Spain solving an inverse problem with a probabilistic model.**\narXiv preprint arXiv:2004.13695.\n\n\nThis model's main goal is to estimate the levels of infections (or the seroprevalence) of the population, using only data from the registered deaths caused by COVID-19. Although the model can be used to make future predictions (evolution of infections, fatalities, etc.), that's not the primary purpose of the model. Given the uncertainty about essential events that alter the course and dynamics of the spread (for example, the use of masks, lockdowns, social distance, etc.), it is tough to make accurate predictions, so we limit ourselves to use the model to reveal more information about what happened before (backcasting).\n",
    'author': 'Pablo R. Mier',
    'author_email': 'pablo.rodriguez-mier@inrae.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/covid19-modeling/pyncov-19',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
