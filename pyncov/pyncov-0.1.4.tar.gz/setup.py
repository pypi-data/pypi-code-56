# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyncov']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1,<2.0.0']

extras_require = \
{'all': ['tqdm>=4.41.0,<5.0.0',
         'pandas>=1.0.0,<2.0.0',
         'matplotlib>=3.2.1,<4.0.0']}

setup_kwargs = {
    'name': 'pyncov',
    'version': '0.1.4',
    'description': 'Pyncov-19 is a tiny probabilistic simulator for SARS-CoV-2',
    'long_description': '# Pyncov-19: Learn and predict the spread of COVID-19\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1LzTsXcisv_v_w4q6o9GxvuAzToExFGaG?usp=sharing)\n\nPyncov-19 is a tiny probabilistic simulator for SARS-CoV-2 implemented in Python 3, whose only dependency is Numpy 1.18.\nThis simulator is used to learn and predict the temporal dynamics of COVID-19 that are shown in https://covid19-modeling.github.io. It implements a probabilistic compartmental model at the individual level using a Markov Chain model with temporal transitions that were adjusted using the most recent scientific evidence.\n\n![](https://github.com/covid19-modeling/pyncov-19/raw/master/notebooks/assets/madrid_example.png)\n\n## Quick Start\n\nBasic installation using pip with minimal dependencies:\n\n```bash\npip install pyncov\n```\n\nIn order to install pyncov with the additional features (progress bar, plotting) use:\n\n```bash\npip install pyncov[all]\n```\n\nSampling 100 simulated trajectories of the SARS-CoV-2 spread in Madrid:\n\n```python\nimport pyncov as nc\nimport pyncov.io\n# Requires pandas\nimport pyncov.plot\n\nsusceptible = 6680000\ninfected = 1\nnum_days = 80\n\nparameters = nc.io.get_trained_params(\'ESP-MD\')\n# Use the default Ri(t) function with the provided parameters to calculate the daily individual dynamic reproduction rate\nvalues = [nc.default_rit_function(i, parameters) for i in range(num_days)]\n\n# Instantiate the model with the default parameters and sample 100 chains\n# NOTE: show_progress requires the TQDM library not installed by default.\nm = nc.build_markovchain(nc.MARKOV_DEFAULT_PARAMS)\nsimulations = nc.sample_chains(susceptible, infected, m, values, \n                               num_chains=100, show_progress=True)\n\n```\n\nYou can visualizate the trajectories and the average trajectory matching the observed values in Madrid using `pyncov.plot`:\n\n```python\nimport matplotlib.pyplot as plt\n\n# Load the dataset with pandas\ndf = pd.read_csv(...)\n\nfig, ax = plt.subplots(1, 3, figsize=(16, 4))\nnc.plot.plot_state(simulations, nc.S.I1, ax=ax[0], index=df.index, title="New infections over time")\nnc.plot.plot_state(simulations, nc.S.M0, diff=True, ax=ax[1], index=df.index, title="Daily fatalities")\nnc.plot.plot_state(simulations, nc.S.M0, ax=ax[2], index=df.index, title="Total fatalities")\ndf.diff().plot(ax=ax[1]);\ndf.plot(ax=ax[2]);\n```\n![](https://github.com/covid19-modeling/pyncov-19/raw/master/notebooks/assets/madrid_example.png)\n\nA more detailed explanation can be found in the notebook included in the repository https://github.com/covid19-modeling/pyncov-19/blob/master/notebooks/basics.ipynb\n\n\n\n## About\n\nThis library is still a proof-of-concept and it\'s inteded only to be used for research and experimentation. For more information please read our [preprint](https://arxiv.org/abs/2004.13695):\n\n> Matabuena, M., Meijide-García, C., Rodríguez-Mier, P., & Leborán, V. (2020). \n**COVID-19: Estimating spread in Spain solving an inverse problem with a probabilistic model.**\narXiv preprint arXiv:2004.13695.\n\n\nThis model\'s main goal is to estimate the levels of infections (or the seroprevalence) of the population, using only data from the registered deaths caused by COVID-19. Although the model can be used to make future predictions (evolution of infections, fatalities, etc.), that\'s not the primary purpose of the model. Given the uncertainty about essential events that alter the course and dynamics of the spread (for example, the use of masks, lockdowns, social distance, etc.), it is tough to make accurate predictions, so we limit ourselves to use the model to reveal more information about what happened before (backcasting).\n',
    'author': 'Pablo R. Mier',
    'author_email': 'pablo.rodriguez-mier@inrae.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/covid19-modeling/pyncov-19',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
