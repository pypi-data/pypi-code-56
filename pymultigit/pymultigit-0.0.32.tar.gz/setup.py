import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pymultigit',
    version='0.0.32',
    packages=[
        'pymultigit',
        'pymultigit.endpoints',
    ],
    # from here all is optional
    description='pymultigit is a command to help you deal with multiple git repositories',
    long_description='pymultigit is a command to help you deal with multiple git repositories',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'git',
        'python',
        'repositories',
        'multiple',
    ],
    url='https://veltzer.github.io/pymultigit',
    download_url='https://github.com/veltzer/pymultigit',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'gitpython',
        'pyfakeuse',
        'pytconf',
        'pylogconf',
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
        'pymultigit=pymultigit.endpoints.main:main',
    ]},
    python_requires='>=3.5',
)
