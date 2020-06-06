
from setuptools import setup, find_namespace_packages


setup(
    name='qtoggleserver-mppsolar',
    version='1.0.0-beta.1',
    description='MPP Solar inverters support for qToggleServer',
    author='Calin Crisan',
    author_email='ccrisan@gmail.com',
    license='Apache 2.0',

    packages=find_namespace_packages(),

    install_requires=[
        'mpp-solar@git+ssh://git@github.com/ccrisan/mpp-solar@0298420de74969c85d470c578df98e359ecb84f0'
    ]
)
