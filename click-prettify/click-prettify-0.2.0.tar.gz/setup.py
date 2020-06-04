from setuptools import setup


with open('README.md', 'r') as f:
    long_description = ''.join(f.readlines()[1:]).lstrip()


setup(
    name='click-prettify',
    version='0.2.0',
    description='Extensions for click to make pretty CLIs in Python',
    long_description=long_description,
    url='https://github.com/jnrbsn/python-click-prettify',
    author='Jonathan Robson',
    author_email='jnrbsn@gmail.com',
    license='MIT',
    py_modules=['click_prettify'],
    install_requires=[
        'click',
        'colorama',
    ],
    extras_require={
        'dev': [
            'flake8',
            'twine'
        ],
    },
)
