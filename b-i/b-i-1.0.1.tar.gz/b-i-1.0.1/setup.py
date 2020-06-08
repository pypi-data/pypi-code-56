__author__ = 'https://cpp.la'


from setuptools import setup, find_packages

files = ["b-i/*"]

setup(
    name='b-i',
    version='1.0.1',
    keywords=['b-i', 'hive', 'mysql', 'elasticsearch', 'cppla'],
    description='python library for data project',
    long_description=(
        "BI tools for data developer use Python Language."
    ),
    license='MIT License',

    author='cppla',
    author_email='i@cpp.la',
    url='https://github.com/cppla/b-i',

    packages=find_packages(),

    platforms='linux',
    install_requires=[
        'sasl',
        'thrift',
        'thrift-sasl',
        'pyhive',
        'requests',
        'sqlalchemy',
        'loguru',
        'python-dateutil',
        'elasticsearch'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires=">=3.6",
)
