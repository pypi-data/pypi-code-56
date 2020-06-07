from setuptools import setup, find_packages

setup(
    name="nl-nut-telegraf",
    version="0.0.1",
    description="Basic NUT Data Exporter for Telegraf",
    author="nonlogicaldev",

    install_requires=[
        "nut2"
    ],

    packages=find_packages(),
    scripts=[
        "bin/nut-telegraf"
    ]
)

