# -*- coding: utf-8-*-
from setuptools import setup, find_packages
setup(
    # 以下为必需参数
    name='scrapy-rabbitmq-scheduler-neo',  # 模块名
    version='1.0.6',  # 当前版本
    description='Rabbitmq for Distributed scraping, copy from scrapy-rabbitmq-scheduler and fix some bugs',  # 简短描述
    author='aox lei',
    author_email='2387813033@qq.com',
    license='MIT',
    url='https://github.com/aox-lei/scrapy-rabbitmq-scheduler',
    install_requires=[
        'pika',
        'Scrapy>=0.14'
    ],
    packages=['scrapy_rabbitmq_scheduler'],
    package_dir={'': 'src'}
)
