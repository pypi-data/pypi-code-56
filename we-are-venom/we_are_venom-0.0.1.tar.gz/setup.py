from typing import Optional

from setuptools import setup, find_packages


package_name = 'we_are_venom'


def get_version() -> Optional[str]:
    with open(f'{package_name}/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


def get_long_description() -> str:
    with open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name=package_name,
    description='Checks which modules developer contributed using git history.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    keywords='plugins git statistics',
    version=get_version(),
    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    install_requires=[
        'setuptools',
        'click>=7.1.2',
        'rich>=1.3.0',
        'gitpython>=3.1.3',
        'unidiff>=0.6.0',
    ],
    entry_points={
        'console_scripts': [
            'venom = we_are_venom.venom:cli',
        ],
    },
    url='https://github.com/best-doctor/we_are_venom',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
