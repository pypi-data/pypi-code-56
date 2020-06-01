# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxawesome_theme']

package_data = \
{'': ['*'], 'sphinxawesome_theme': ['static/*']}

install_requires = \
['sphinx>3']

entry_points = \
{'sphinx.html_themes': ['sphinxawesome_theme = sphinxawesome_theme']}

setup_kwargs = {
    'name': 'sphinxawesome-theme',
    'version': '1.5.0',
    'description': 'A simple theme for a Sphinx documentation',
    'long_description': '====================\nSphinx awesome theme\n====================\n   \n.. image:: https://img.shields.io/pypi/l/sphinxawesome-theme?color=blue&style=for-the-badge\n   :target: https://opensource.org/licenses/MIT\n   :alt: MIT license\n   \n.. image:: https://img.shields.io/pypi/v/sphinxawesome-theme?style=for-the-badge\n   :target: https://pypi.org/project/sphinxawesome-theme\n   :alt: PyPI package version number\n\n.. image:: https://img.shields.io/netlify/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22?style=for-the-badge\n   :target: https://sphinxawesome.xyz\n   :alt: Netlify Status\n\nThis is a simple but awesome theme for the `Sphinx\n<http://www.sphinx-doc.org/en/master/>`_ documentation generator.\n\n\n------------\nInstallation\n------------\n\nInstall the theme as a Python package:\n\n.. install-start\n\n.. code:: console\n\n   pip install sphinxawesome-theme\n\n.. install-end\n\nRead the full `installation instructions\n<https://sphinxawesome.xyz/docs/install.html#how-to-install-the-theme>`_ for more\ninformation.\n\n-----\nUsage\n-----\n\n.. use-start\n\nTo use the theme, set ``html_theme`` in the Sphinx configuration file\n``conf.py``:\n\n.. code:: python\n\n   html_theme = "sphinxawesome_theme"\n\n.. use-end\n\nRead the full `usage guide\n<https://sphinxawesome.xyz/docs/use.html#how-to-use-the-theme>`_ for more information.\n\n----\nDemo\n----\n\nSee how the theme looks on the `demo page <https://sphinxawesome.xyz>`_.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-theme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
