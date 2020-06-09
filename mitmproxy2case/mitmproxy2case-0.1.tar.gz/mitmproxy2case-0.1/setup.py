from setuptools import setup

setup(
    name='mitmproxy2case',
    version='0.1',
    author='T8840',
    url='https://github.com/T8840/mitmproxy2case',
    py_modules=['mitmproxy2case'],
    install_rpequires=[
        'Click',
        'mitmproxy',
        'PyYaml'
    ],
    entry_points={
        'console_scripts': [
            'mitmproxy2case=mitmproxy2case.cli:main'
        ]
    }

)