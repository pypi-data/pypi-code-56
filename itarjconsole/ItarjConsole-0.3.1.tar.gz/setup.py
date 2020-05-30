import setuptools


setuptools.setup(
    name="ItarjConsole", # Replace with your own username
    version="0.3.1",
    author="Uchegbu Damianson-Wisdom",
    author_email="damiansonuchegbu2017@gmail.com",
    description="A CLI application created with Python that allows users to create posts of fake job alerts and allows user to also search the database for these posts using keywords",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/startng/forward-itarj-damianson",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['click','pyfiglet','mysql-connector-python','colorama'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)