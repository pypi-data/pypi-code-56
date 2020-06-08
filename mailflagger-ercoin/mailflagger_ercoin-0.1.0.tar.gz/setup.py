from setuptools import find_namespace_packages, setup


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mailflagger_ercoin',
    version='0.1.0',
    description='An Ercoin plugin for Mail Flagger',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='krzysztof.jurewicz@gmail.com',
    packages=find_namespace_packages(),
    python_requires='>=3.8, <4',
    keywords='cryptocurrency',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: AsyncIO',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Email :: Filters',
    ],
    install_requires=[
        'ern_reactor',
        'mailflagger',
    ],
    entry_points={
        'mailflagger.plugins.daemon': [
            'ercoin = mailflagger.plugins.ercoin',
        ],
    },
)
