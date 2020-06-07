from setuptools import setup, find_packages

setup(
    name="nl-nut-telegraf",
    version="0.0.3",
    description="Basic NUT Data Exporter for Telegraf",
    author="nonlogicaldev",

    install_requires=[
        "nut2",
        "influxdb"
    ],

    packages=find_packages(),
    scripts=[
        "bin/nut-telegraf"
    ]
)

