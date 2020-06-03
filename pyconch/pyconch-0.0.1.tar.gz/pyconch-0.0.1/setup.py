import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pyconch',
    version='0.0.1',
    packages=[
    ],
    # from here all is optional
    description='Pyconch is a wrapper for a shell in python',
    long_description='Pyconch is a wrapper for a shell in python',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'make',
        'scons',
    ],
    url='https://veltzer.github.io/pyconch',
    download_url='https://github.com/veltzer/pyconch',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
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
        'pyconch=pyconch.endpoints.main:main',
    ]},
    python_requires='>=3.5',
)
