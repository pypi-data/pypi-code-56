# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pr0cks']

package_data = \
{'': ['*']}

install_requires = \
['PySocks>=1.7.1,<2.0.0', 'pr0cks-extension>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['pr0cks = pr0cks.console:main']}

setup_kwargs = {
    'name': 'pr0cks',
    'version': '0.2.0',
    'description': 'Transparent proxy in python',
    'long_description': "# pr0cks\npython script to transparently forward all TCP traffic through a socks (like ssh -D option) or HTTPS (CONNECT) proxy using iptables -j REDIRECT target. Only works on linux for now.\n\n## Features :\n- set up a local transparent proxy compatible with socks4 socks5 and HTTP CONNECT proxies allowing to forward any TCP traffic transparently using iptables\n<!-- TODO make sure this works\n- set up a local transparent DNS proxy translating UDP port 53 requests to TCP allowing DNS traffic to go through a proxy without UDP support (like ssh -D option)\n- DNS caching mechanism to speed up the DNS resolutions through pr0cks\n-->\n# Usage example: let's rock\nAs an example we will use the socks5 proxy of openssh (the option -D)\n```bash\n$ ssh -D 1080 user@sshserver\n```\nthen you can add some iptables rules :\n```bash\n$ iptables -t nat -A OUTPUT ! -d <my_ssh_server_IP>/32 -o eth0 -p tcp -m tcp -j REDIRECT --to-ports 10080\n```\nthen start pr0cks :\n```bash\n$ pr0cks --proxy SOCKS5:127.0.0.1:1080\n```\nAll your TCP traffic and DNS traffic should now pass through the ssh server kinda like if you had setup a tun VPN through ssh but without admin rights on the server !\n#help\n```text\npr0cks -h\nusage: procks [-h] [--type {HTTP,SOCKS4,SOCKS5}] [-p PORT] [-n] [-v] [-c]\n              [--username USERNAME] [--password PASSWORD]\n              proxy_addr proxy_port\n\nTransparent SOCKS5/SOCKS4/HTTP_CONNECT Proxy\n\npositional arguments:\n  proxy_addr\n  proxy_port\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --type {HTTP,SOCKS4,SOCKS5}\n                        The type of proxy to forward the traffic to\n  -p PORT, --port PORT  port to bind the transparent proxy on the local socket\n                        (default 10080)\n  -n, --nat             set bind address to 0.0.0.0 to make pr0cks work from a\n                        netfilter FORWARD rule instead of OUTPUT\n  -v, --verbose         print all the connections requested through the proxy\n  -c, --no-cache        don't cache dns requests\n  --username USERNAME   Username to authenticate with to the server. The\n                        default is no authentication.\n  --password PASSWORD   Only relevant when a username has been provided\n```\n\n# Dependencies\n- tested with Python 3.6\n\n# TODO\n- support UDP (with socks5)\n- support proxy chaining\n\n\nDon't hesitate to send me your feedback or any issue you may find\n\nI hope it will be useful to someone ! Have fun :)\n",
    'author': 'Nicolas VERDIER',
    'author_email': 'contact@n1nj4.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/NamingThingsIsHard/net/pr0cks/pr0cks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
