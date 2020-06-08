from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

requirements = []

setup(
    name='jupy-wrapper',
    version='0.0.2',
    author='AlexKalopsia',
    author_email='camilleri.alex@gmail.com',
    description='A package to convert Jupiter Notebooks',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/AlexKalopsia/jupy-wrapper',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ]
)
