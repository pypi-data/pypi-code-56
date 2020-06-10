from setuptools import setup, find_packages

setup(
    name                = 'chatchecker',
    version             = '0.1.7',
    description         = 'chatchecker',
    author              = 'Seoyoung Hong',
    author_email        = 'seoyoungh@khu.ac.kr',
    url                 = 'https://github.com/seoyoungh/ko-chat-checker',
    download_url        = 'https://github.com/seoyoungh/ko-chat-checker',
    install_requires    = ['chatspace'],
    packages            = find_packages(exclude = []),
    keywords            = ['chatchecker'],
    python_requires     = '>=3',
    package_data        = {},
    include_package_data = True,
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
