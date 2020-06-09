from setuptools import setup, Extension

with open('README.md', encoding='utf8') as f:
    readme = f.read()

setup(
    name='pygopac',
    version='0.1.0',
    url='https://bitbucket.org/alex925/py-gopac/src/master/',
    author='Aleksey Petrunnik',
    author_email='petrunnik.a@mail.ru',
    description='Python library to parse proxy auto-config (PAC) files.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['gopac'],
    install_requires=['requests>=2.18.4'],
    setup_requires=['setuptools-golang-cli', 'wheel'],
    dependency_links=[
        'git+https://alex925@bitbucket.org/alex925/setuptools-golang-cli.git@master#egg=setuptools-golang-cli'
    ],
    ext_modules=[
        Extension(
            'gopac.extension.gopaccli',
            ['extension/src/gopaccli/gopaccli.go']
        ),
    ],
    build_golang_cli={'root': 'extension'},
)
