# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxawesome', 'sphinxawesome.sampdirective']

package_data = \
{'': ['*']}

install_requires = \
['sphinx>=2.2']

setup_kwargs = {
    'name': 'sphinxawesome-sampdirective',
    'version': '1.0.0',
    'description': 'A Sphinx directive for literal blocks with emphasis',
    'long_description': '# Sphinx Awesome Sampdirective\n\n![GitHub](https://img.shields.io/github/license/kai687/sphinxawesome-sampdirective?color=blue&style=for-the-badge)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kai687/sphinxawesome-sampdirective/Run%20unit%20tests?style=for-the-badge)\n![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)\n\nThis Sphinx extension provides a new directive `.. samp::` which works much like the\ninterpreted text role\n[samp](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-samp).\nThis extension can be used to markup placeholder variables in code blocks.\n\n## Installation\n\nInstall the extension:\n\n```console\npip install sphinxawesome-sampdirective\n```\n\nThis Sphinx extension should work with Python versions newer than 3.6 and recent Sphinx\nreleases.\n\n## Configuration\n\nTo enable this extension in Sphinx, add it to the list of extensions in the Sphinx\nconfiguration file `conf.py`:\n\n```python\nextensions = ["sphinxawesome.sampdirective"]\n```\n\n## Use\n\nInclude the directive in your documents:\n\n```\n.. samp::\n\n   $ echo {USERNAME}\n```\n\n`USERNAME` will become an _emphasized_ node. In many outputs, it will be rendered as\n_`USERNAME`_. For example, in HTML, the above example will be rendered as:\n\n```HTML\n<pre>\n    <span class="gp">$</span> echo <em class="var">USERNAME</em>\n</pre>\n```\n\nYou can then control the style of the emphasized element with the `.var` class in CSS.\nIf the code block begins with a prompt character (`#`, `$`, or `~`), they will be marked\nup as well. The style for the prompt character is provided by the `pygments` syntax\nhighlighting module.\n\nThe [sphinxawesome theme](https://github.com/kai687/sphinxawesome-theme) includes\nstyling for the `..samp::` directive.\n\n## Caveat\n\nThis extension does not provide full syntax highlighting. It is currently not possible\nto have code blocks with both markup _and_ syntax highlighting. If you need to render\nmarkup, for example links, or bold or italic text, choose the `.. parsed-literal::`\ndirective. If you just want to highlight a placeholder variable, use the `.. samp::`\ndirective provided by this extension. If you need full syntax highlighting, use the\n`.. code-block::` directive.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-sampdirective',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
