from setuptools import setup

setup(
    name='mitmproxy2case',
    version='0.2.1',
    author='T8840',
    url='https://github.com/T8840/mitmproxy2case',
    install_rpequires=[
        'Click',
        'mitmproxy',
        'PyYaml'
    ],
    entry_points={
        'console_scripts': [
            'mitmproxy2case=mitmproxy2case.mitmproxy2case:cli'
        ]
    }

)