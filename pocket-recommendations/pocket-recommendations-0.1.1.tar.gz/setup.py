# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pocket_recommendations']
install_requires = \
['cssselect>=1.1.0,<2.0.0', 'lxml>=4.5.1,<5.0.0']

setup_kwargs = {
    'name': 'pocket-recommendations',
    'version': '0.1.1',
    'description': "Unofficial library to get a feed of one's Pocket recommendations",
    'long_description': '# pocket-recommendations\n\nUnofficial library to get a feed of one\'s Pocket recommendations\n\n\n## Usage\n\nGet a public Pocket profile, like [this one](https://getpocket.com/@honzajavorek). Download its HTML using Python or anything else:\n\n```bash\n$ curl "https://getpocket.com/@honzajavorek" > getpocket-com-honzajavorek.html\n\n```\n\nIn your Python program, have the HTML ready as a string:\n\n```python\n>>> from pathlib import Path\n>>> html_text = Path(\'getpocket-com-honzajavorek.html\').read_text()\n\n```\n\nNow you can use this library to parse the HTML:\n\n```python\n>>> import pocket_recommendations\n>>> items = pocket_recommendations.parse(html_text)\n>>> len(items)\n50\n\n```\n\nEach item then looks like this:\n\n```python\n>>> from pprint import pprint\n>>> pprint(items[0])\n{\'pocket_comment\': \'\xc5\xa0ablona na v\xc3\xa1\xc5\xa1 \xc3\xbasp\xc4\x9b\xc5\xa1n\xc3\xbd HackerNews post\',\n \'pocket_recommended_at\': None,\n \'pocket_url\': \'https://getpocket.com/redirect?&url=https%3A%2F%2Fsaagarjha.com%2Fblog%2F2020%2F05%2F10%2Fwhy-we-at-famous-company-switched-to-hyped-technology%2F&h=eff6d8cac22c9b475463d037037b0efdcf44b762c9b0b7913de2104cab5fa67d\',\n \'title\': \'Why we at $FAMOUS_COMPANY Switched to $HYPED_TECHNOLOGY\',\n \'url\': \'https://saagarjha.com/blog/2020/05/10/why-we-at-famous-company-switched-to-hyped-technology/\'}\n\n```\n\nEven though Pocket uses HTTP links for the redirects, the library forces HTTPS.\n\n\n### Date of Recommendation\n\nYou can specify the date when the HTML has been downloaded to get the relative dates when the recommendations have been posted:\n\n```python\n>>> from datetime import date\n>>> items = pocket_recommendations.parse(html_text, today=date(2020, 6, 3))\n>>> pprint(items[0])\n{\'pocket_comment\': \'\xc5\xa0ablona na v\xc3\xa1\xc5\xa1 \xc3\xbasp\xc4\x9b\xc5\xa1n\xc3\xbd HackerNews post\',\n \'pocket_recommended_at\': datetime.date(2020, 6, 2),\n \'pocket_url\': \'https://getpocket.com/redirect?&url=https%3A%2F%2Fsaagarjha.com%2Fblog%2F2020%2F05%2F10%2Fwhy-we-at-famous-company-switched-to-hyped-technology%2F&h=eff6d8cac22c9b475463d037037b0efdcf44b762c9b0b7913de2104cab5fa67d\',\n \'title\': \'Why we at $FAMOUS_COMPANY Switched to $HYPED_TECHNOLOGY\',\n \'url\': \'https://saagarjha.com/blog/2020/05/10/why-we-at-famous-company-switched-to-hyped-technology/\'}\n\n```\n\n\n### Missing Comment\n\nIf there is no comment, it is set to `None`:\n\n```python\n>>> from datetime import date\n>>> items = pocket_recommendations.parse(html_text)\n>>> pprint(items[15])\n{\'pocket_comment\': None,\n \'pocket_recommended_at\': None,\n \'pocket_url\': \'https://getpocket.com/redirect?&url=https%3A%2F%2Falmad.blog%2Fessays%2Fwhat-is-employment%2F&h=ef4216c9df41763fa900b12815a280bf790f50960468a45ebed5f3682156dc6a\',\n \'title\': "We Don\'t Know What an Employment Is",\n \'url\': \'https://almad.blog/essays/what-is-employment/\'}\n\n```\n\n\n### Misinterpreted HTML Entities\n\nIf the title contains some misinterpreted HTML entities, the library takes care of it:\n\n```python\n>>> from datetime import date\n>>> items = pocket_recommendations.parse(html_text)\n>>> pprint(items[15])  # title: We Don&#039;t Know What an Employment Is\n{\'pocket_comment\': None,\n \'pocket_recommended_at\': None,\n \'pocket_url\': \'https://getpocket.com/redirect?&url=https%3A%2F%2Falmad.blog%2Fessays%2Fwhat-is-employment%2F&h=ef4216c9df41763fa900b12815a280bf790f50960468a45ebed5f3682156dc6a\',\n \'title\': "We Don\'t Know What an Employment Is",\n \'url\': \'https://almad.blog/essays/what-is-employment/\'}\n\n```\n',
    'author': 'Honza Javorek',
    'author_email': 'mail@honzajavorek.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honzajavorek/pocket-recommendations',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
