# -*- coding: utf-8 -*-
# @Time    : 2020-06-01 16:02
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : setup.py

from setuptools import setup

setup(
    name='PyBuilder-exe',           # 包名
    version='0.1.0',                # 版本信息
    author='leocll',                # 作者
    author_email='leocll@qq.com',   # 邮箱
    description='Build a python program as exe.',
    license='MIT',
    packages=['PyBuilder'],         # 要打包的项目文件夹
    include_package_data=True,      # 自动打包文件夹内所有数据
    zip_safe=True,                  # 设定项目包为安全，不用每次都检测其安全性
    install_requires=[              # 依赖包
        'Cython',
        'PyInstaller',
    ],
    # 设置程序的入口为pybuilder
    # 安装后，命令行执行pybuilder相当于调用main.py文件的run方法
    entry_points={
        'console_scripts': [
            'PyBuilder = PyBuilder.main:run',
        ]
    },
    url='https://github.com/leocll/PyBuilder',
    keywords='PyBuilder pybuilder py2exe exe',
    python_requires='>=3.6'
)

if __name__ == '__main__':
    pass