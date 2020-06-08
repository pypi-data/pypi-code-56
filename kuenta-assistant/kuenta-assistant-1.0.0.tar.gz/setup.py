import setuptools


setuptools.setup(
    name="kuenta-assistant", # Replace with your own username
    version="1.0.0",
    author="Stevenson Marquez",
    author_email="smarquez@kuenta.co",
    description="kuenta api assistant command line client",
    url="https://git1-co.kuenta.net/yaien/kuenta-assistant",
    download_url="https://git1-co.kuenta.net/yaien/kuenta-assistant/-/archive/v1.0.0/kuenta-assistant-v1.0.0.tar.gz",
    py_modules=['main', 'client', 'config'],
    entry_points='''
        [console_scripts]
        kuenta-assistant=main:root
    ''',
    install_requires=[
        'click',
        'requests',
        'configparser'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)