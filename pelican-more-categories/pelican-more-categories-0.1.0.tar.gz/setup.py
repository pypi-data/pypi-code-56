# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.more_categories']

package_data = \
{'': ['*'], 'pelican.plugins.more_categories': ['test_data/*']}

install_requires = \
['pelican>=4.2,<5.0']

extras_require = \
{'markdown': ['markdown>=3.1.1,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-more-categories',
    'version': '0.1.0',
    'description': 'Enables nested categories and multiple categories per article',
    'long_description': '# more-categories\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/more-categories/build)](https://github.com/pelican-plugins/more-categories/actions)\n\nThis plugin adds support for multiple categories per article, and for nested\ncategories. It requires Pelican 4.0.0 or newer.\n\n## Multiple categories\nTo indicate that an article belongs to multiple categories, use a\ncomma-separated string:\n\n    Category: foo, bar, bazz\n\nThis will add the article to the categories `foo`, `bar` and `bazz`.\n\n### Templates\nExisting themes that use `article.category` will display only the first of\nthese categories, `foo`. This plugin adds `article.categories` that you can\nloop over instead. To accomodate this plugin in a theme whether it is present\nor not, use:\n\n    {% for cat in article.categories or [article.category] %}\n        <a href="{{ SITEURL }}/{{ cat.url }}">{{ cat }}</a>{{ \', \' if not loop.last }}\n    {% endfor %}\n\n## Nested categories\n(This is a reimplementation of the `subcategory` plugin.)\n\nTo indicate that a category is a child of another category, use a\nslash-separated string:\n\n    Category: foo/bar/bazz\n\nThis will add the article to the categories `foo/bar/bazz`, `foo/bar` and\n`foo`.\n\n### Templates\nExisting themes that use `article.category` will display the full path to the\nmost specific of these categories, `foo/bar/bazz`. For any category `cat`, this\nplugin adds `cat.shortname`, which in this case is `bazz`, `cat.parent`, which\nin this case is the category `foo/bar`, and `cat.ancestors`, which is a list of\nthe category\'s ancestors, ending with the category itself. For instance, to\nalso include a link to each of the ancestor categories on an article page, in\ncase this plugin in present, use:\n\n    {% for cat in article.category.ancestors or [article.category] %}\n        <a href="{{ SITEURL }}/{{ cat.url }}">{{ cat.shortname or cat }}</a>{{ \'/\' if not loop.last }}\n    {% endfor %}\n\nLikewise, `category.shortname`, `category.parent` and `category.ancestors` can\nalso be used on the category template.\n\nAdditionally, this plugin adds `category.children`: a `list` of categories\nthat have `category` as a parent.\n\n    {% for child in category.children %}\n        <a href="{{ SITEURL }}/{{child.url}}">{{child.shortname|capitalize}}</a>\n    {% endfor %}\n\nIf you need all descendents and not just the immediate children, you can use the `list` of descendents: `category.descendents`.\n\n### Slug\nThe slug of a category is generated recursively by slugifying the shortname of\nthe category and its ancestors, and preserving slashes:\n\n    slug-of-(foo/bar/baz) := slug-of-foo/slug-of-bar/slug-of-baz\n\n### Category folders\nTo specify categories using the directory structure, you can configure\n`PATH_METADATA` to extract the article path into the `category` metadata. The\nfollowing settings would use the entire structure:\n\n    PATH_METADATA = \'(?P<category>.*)/.*\'\n\nIf you store all articles in a single `articles/` folder that you want to\nignore for this purpose, use:\n\n    PATH_METADATA = \'articles/(?P<category>.*)/.*\'\n\n### Categories in templates\nThe list `categories` of all pairs of categories with their corresponding\narticles, which is available in the context and can be used in templates (e.g.\nto make a menu of available categories), is ordered lexicographically, so\ncategories always follow their parent:\n\n    aba\n    aba/dat\n    abaala\n',
    'author': 'Oliver Urs Lenz',
    'author_email': 'oliver.urs.lenz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/more-categories',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
