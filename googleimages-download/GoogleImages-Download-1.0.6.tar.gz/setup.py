from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="GoogleImages-Download",
    version="1.0.6",
    description="A Python Script for downloading bulk of images from google.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/khannoaman/GoogleImages-Download",
    author="MOHAMMAD NOAMAN KHAN",
    author_email="khan.noamaan@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["GoogleImages_Download"],
    include_package_data=True,
    install_requires=["requests","selenium","tqdm","chromedriver_binary","chromedriver_binary==83.0.4103.39.0"],
    entry_points={
        "console_scripts": [
            "GoogleImages-Download=GoogleImages_Download.GoogleImagesDownload:main",
        ]
    },
)