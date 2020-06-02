# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['async_weather_sdk']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'async-weather-sdk',
    'version': '0.1.1',
    'description': 'Async weather API wrapper for fetching weather and forecast data',
    'long_description': "# Async Weather SDK\n\n[![PyPI version](https://img.shields.io/pypi/v/async-weather-sdk?logo=python&logoColor=white)](https://badge.fury.io/py/async-weather-sdk)\n[![GitHub Workflow Status for tests](https://img.shields.io/github/workflow/status/decentfox/async-weather-sdk/test?logo=github&logoColor=white)](https://github.com/decentfox/async-weather-sdk/actions?query=workflow%3Atest)\n[![Codacy Badge](https://img.shields.io/codacy/coverage/f548667427c24fc394204b440166c26d?logo=Codacy)](https://www.codacy.com/gh/decentfox/async-weather-sdk?utm_source=github.com&utm_medium=referral&utm_content=decentfox/async-weather-sdk&utm_campaign=Badge_Coverage)\n\nAsync weather API wrapper for fetching weather and forecast data\n\n## Core Dependencies\n\n**Asyncio:** a library to write concurrent code using the async/await syntax.\n\n**Aiohttp:** an asynchronous HTTP Client/Server for asyncio and Python.\n\n## Install\n\n```bash\npip install async-weather-sdk\n\nOR\n\npoetry add async-weather-sdk\n```\n\n## Usage\n\n### QQ Weather API SDK\n\nGet current weather/forecast data by province and city.\n\n```python\nfrom async_weather_sdk.qq import QQWeather\n\nweather = QQWeather()\n\nawait weather.fetch_current_weather('北京市', '北京市')\nawait weather.fetch_weather_forecast('北京市', '北京市', 3)\n```\n\nQuery current weather/forecast data with tencent map api key.\n\n```python\nfrom async_weather_sdk.qq import query_current_weather, query_weather_forecast\n\nawait query_current_weather('API_KEY', '北京市')\nawait query_weather_forecast('API_KEY', '39.90469,116.40717')\n```\n",
    'author': 'DecentFoX',
    'author_email': 'service@decentfox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decentfox/async-weather-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
