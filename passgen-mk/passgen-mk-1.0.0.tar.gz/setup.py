import fnmatch
from os import path
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as build_py_orig

import passgen

exclude = ['passgen.*_test']

# https://stackoverflow.com/questions/50506072/exclude-single-source-file-from-python-bdist-egg-or-bdist-wheel#answer-50517893
class build_py(build_py_orig):
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return [(pkg, mod, file, ) for (pkg, mod, file, ) in modules
                if not any(fnmatch.fnmatchcase(pkg + '.' + mod, pat=pattern)
                for pattern in exclude)]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='passgen-mk',
    version=passgen.__version__,
    description='Generates a password consisting of selected characters and the specified length.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Environment :: Console',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security :: Cryptography',
        'Intended Audience :: Developers',
    ],
    keywords='console password-generator',
    url='https://gitlab.com/marekkon/passgen',
    author='Marek Konopka',
    author_email='git@marek-konopka.com',
    license='ICS',
    packages=find_packages(),
    cmdclass={'build_py': build_py},
    entry_points={
        'console_scripts': [
            'passgen=passgen.cli:main'
        ]
    },
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'flake8'
        ]
    }
)
