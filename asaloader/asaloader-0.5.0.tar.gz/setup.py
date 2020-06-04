# -*- coding: utf-8 -*-

import os
import asaloader

import setuptools
import utils.l10n


# 將所有.po編譯成.mo
utils.l10n.create_mo_files()

# 取得所有翻譯相關檔案，包括 .mo, .po, .pot
l10n_files = utils.l10n.get_l10n_files()

# 將檔案列表包裝成 setuptools 接收之格式
# data_files specifies a sequence of (directory, files)
data_files = [(os.path.split(f)[0], [f]) for f in l10n_files]

# 讀取模組說明
with open('readme.md', 'r') as f:
    long_description = f.read()

# 讀取需求模組列表
with open('requirement.txt','r') as f:
    install_requires = f.read().split('\n')
    install_requires.remove('')


setuptools.setup(
    name='asaloader',
    version=asaloader.__version__,
    description='The program to load binary into ASA series board.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MVMC-lab',
    author_email='ncumvmclab@gmail.com',
    url='https://gitlab.com/MVMC-lab/hervor/asaloader',
    license='MIT',
    packages=['asaloader'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'asaloader = asaloader.__main__:run'
        ],
    },
    data_files=data_files,
    install_requires=install_requires
)
