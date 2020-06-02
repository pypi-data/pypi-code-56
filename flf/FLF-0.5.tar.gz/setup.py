from distutils.core import setup


setup(
    name = "FLF",
    packages = ["FLF"],
    version = "0.5",
    license="MIT",
    description = "Server and Connector for RabbitMQ",
    author = "DenisVASI9",
    author_email = "gkanafing@gmail.com",
    url = "https://github.com/DenisVASI9/FLF",
    download_url = "https://github.com/DenisVASI9/FLF/archive/0.5.tar.gz",
    keywords = ["RabbitMQ", "RPCServer", "RPCConnector", "pika"],
    install_requires=[
        "pika"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    )