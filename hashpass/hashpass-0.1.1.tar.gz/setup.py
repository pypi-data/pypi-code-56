# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['main']
install_requires = \
['gooey>=1.0.3,<2.0.0', 'pyinstaller>=3.6,<4.0', 'pyperclip>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'hashpass',
    'version': '0.1.1',
    'description': '哈希密码生成程序',
    'long_description': '# hashpass\n\n> 哈希密码生成程序\n\n## 关于 hashpass\n\n如果所有的网站都使用同一个密码毫无疑问是非常不安全的, 密码一旦丢失所有账号都会被一锅端. 常见的处理方法是生成随机密码, 目前有很多软件和应用可以做到, 但随机密码有个不好的地方, 密码非常难记需要有个地方储存密码, 你可以保存到云上或者本地, 但这又产生信任和丢失的问题. 于是我想用一种尽可能简单的方法, 来生成复杂同时又不需要储存的密码, 那就是记住一个盐值, 然后生成哈希密码.\n\n## 算法\n\n1. 将输入的域名(`domain`)与环境变量设置的盐(`HASHPASS_SALT`)进行字符串拼接\n2. 拼接得到的字符串使用 `SHA-256` 算法加密\n3. 然后把得到的哈希值进行 `base64` 编码\n4. 截取前`length`个字符串, 返回结果\n\n## 使用\n\n输入域名和密码长度, 点击开始, 程序会自动复制结果到剪贴板, 直接 `CTRL + V` 即可\n\n## 打包程序\n\n```bash\npip install -r requirements.txt\npyinstaller -Fw main.py\n```\n',
    'author': 'guaifish',
    'author_email': 'guaifish@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guaifish/hashpass',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
