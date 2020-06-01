import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pypathutil',
    version='0.0.12',
    packages=[
        'pypathutil',
        'pypathutil.endpoints',
    ],
    # from here all is optional
    description='command line utilities to help you work with paths',
    long_description='command line utilities to help you work with paths',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'path',
        'command line',
        'shell',
        'reduce',
        'append',
        'remove',
    ],
    url='https://veltzer.github.io/pypathutil',
    download_url='https://github.com/veltzer/pypathutil',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'pylogconf',
        'pytconf',
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
        'pypathutil=pypathutil.endpoints.main:main',
    ]},
    python_requires='>=3.4',
)
