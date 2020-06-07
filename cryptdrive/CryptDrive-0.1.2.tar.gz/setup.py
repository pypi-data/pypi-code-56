import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CryptDrive",
    version="0.1.2",
    author="revanrohith",
    author_email="revanrohith@gmail.com",
    description="A Simple Encryption Tool that also saves and retreive files from Google Drive with OneLine-Commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/revanrohith/CryptDrive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'google-auth-oauthlib==0.4.1',
        'cryptography==2.9.2',
        'oauth2client==4.1.3',
        'google-api-python-client==1.9.1'
    ],
    python_requires='>=3.6',
)