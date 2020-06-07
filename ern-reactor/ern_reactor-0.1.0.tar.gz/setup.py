from setuptools import setup


with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='ern_reactor',
    version='0.1.0',
    description='Do arbitrary things in reaction to Ercoin transfers',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/KrzysiekJ/ern_reactor',
    author='Krzysztof Jurewicz',
    author_email='krzysztof.jurewicz@gmail.com',
    python_requires='>=3.8, <4',
    keywords='cryptocurrency',
    py_modules=['ern_reactor'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['websockets>=8, <9'],
)
