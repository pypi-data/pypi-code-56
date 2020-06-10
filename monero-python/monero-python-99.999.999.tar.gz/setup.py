from setuptools import setup

readme = open("README.md").read()

setup(
    name="monero-python",
    version="99.999.999",
    author="Gonçalo Valério",
    author_email="gon@ovalerio.net",
    url="",
    description="Empty package",
    long_description=readme,
    license='BSD-3-Clause',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=["monero"],
    include_package_data=True,
)
