# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['signpost']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1,<2.0.0', 'pandas>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'signpost',
    'version': '0.1.0',
    'description': 'Simple decorators and functions for type checking pandas DataFrames at runtime',
    'long_description': 'signpost\n========\n\nThis is a simple library for annotating and enforcing properties of\npandas DataFrames at runtime. By showing which columns and types\nare expected before execution of a function begins, we can catch errors\nearlier with a message that makes sense and also document the inputs and\noutputs of functions more concisely.\n\n\nExample Usage\n-------------\n\nHere is an example of standard usage to decorate a fairly strange function.\nNote that any valid pandas index value can be used, including numbers. We\ncan combine ``Property``\'s together using ``And`` and ``Or`` if desired\nas well as qualify them using "all", "any", "just", or "none".\n\n.. code-block:: python\n\n    from signpost import Cols, Schema, Values, Superkey, And, df_args, df_return\n\n    @df_args(\n        And(Cols("all", ["thing_1", 2]), Superkey(["thing_1"], over=[2])),\n        other=Schema("just", {"thing_2": int, "thing_3": "string"})\n    )\n    @df_return(\n        None,\n        And(\n            Cols("all", ["thing_1", "thing_2", "thing_3"]),\n            Values("any", {"thing_1": [1, 2], "thing_3": ["foo", "bar"]}),\n            Values("none", {"thing_1": [3]}),\n        )\n    )\n    def do_a_thing(df: pd.DataFrame, other: pd.DataFrame) -> (int, pd.DataFrame):\n        ...\n\nHowever, there are times when the particular properties of a data frame depend on other\ninputs to a function. For example, a function may take a list of columns to subset\nby or a set of values to query with. This behavior is somewhat analogous to a function\ntaking a ``List[T]`` and a parameter of type ``T`` – we are essentially making the data\nframe generic over a parameter specified by the caller. In these cases, we can\nuse the ``Meta`` constructor, which is constructed with a string of Python code.\nThe code is then evaluated with the environment of the function.\nFor example, we can implement a checked "project" function\n(analogous to ``SELECT DISTINCT`` in SQL) as follows:\n\n.. code-block:: python\n\n    from signpost import df_args, df_return, Cols, Meta\n\n    @df_args(Cols("all", Meta("cols")))\n    @df_return(Cols("just", Meta("cols")))\n    def project(df: pd.DataFrame, cols: List[str]):\n        return df.loc[:, cols].drop_duplicates()\n\nSince the expressions passed to these meta properties can be arbitrary Python strings,\nwe can express some fairly powerful logic using relatively little code. Note that\nsince pandas DataFrames are dict-like, we can treat them as sequences of column names.\n\n.. code-block:: python\n\n    from signpost import df_args, df_return, Cols, Meta\n\n    @df_args(left=Cols("any", Meta("right")), right=Cols("any", Meta("left")))\n    @df_return(Cols("just", Meta("set(left) | set(other)"))\n    def merge(left, right):\n        return pd.merge(left, right)\n\nExtending signpost\n------------------\nThere are a couple of ways to extend signpost. The first is using the ``Function`` property.\nIt simply accepts a function that takes a pandas DataFrame and a context dictionary and returns\na ``Optional[str]``.\n\n.. code-block:: python\n\n    from signpost import df_args, Function\n\n    @df_args(Function(lambda df, context: "bad" if df.empty else None))\n    def do_another_thing(df: pd.DataFrame):\n        ...\n\nIt is also possible to create new ``Property``\'s simply by implementing the ``Property``\nor ``ContextProperty`` interface found in ``signpost.properties``.\n\n\nTODO\n----\nThere are a couple of improvements to be made, namely\n\n1. **Ergonomics.** Assume bare types to be single-element lists.\n\n2. **Documentation.**',
    'author': 'Ilse Dippenaar',
    'author_email': 'ilsedipp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
