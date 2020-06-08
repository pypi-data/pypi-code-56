from setuptools import setup, find_packages

setup(
    name='configger',
    version='0.0.1',
    url='https://github.com/paulharter/configger.git',
    author='Paul Harter',
    author_email='paul@glowinthedark.co.uk',
    license="LICENSE",
    description='Simple config',
    packages=find_packages('src'),
    package_dir={'configger': 'src/configger'},
    install_requires=[]
)