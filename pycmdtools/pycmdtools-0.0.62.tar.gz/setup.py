import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pycmdtools',
    version='0.0.62',
    packages=[
        'pycmdtools',
        'pycmdtools.endpoints',
    ],
    # from here all is optional
    description='pycmdtools is set of useful command line tools written in python',
    long_description='pycmdtools is set of useful command line tools written in python',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'utils',
        'command line',
        'python',
        'shell',
        'utilities',
    ],
    url='https://veltzer.github.io/pycmdtools',
    download_url='https://github.com/veltzer/pycmdtools',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'pylogconf',
        'pytconf',
        'requests',
        'tqdm',
        'numpy',
        'pandas',
        'unidecode',
        'pyyaml',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    data_files=[
    ],
    entry_points={'console_scripts': [
        'pycmdtools=pycmdtools.endpoints.main:main',
    ]},
    python_requires='>=3.5',
)
