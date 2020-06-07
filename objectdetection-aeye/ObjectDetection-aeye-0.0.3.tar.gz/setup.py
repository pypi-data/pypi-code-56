import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ObjectDetection-aeye", # Replace with your own username
    version="0.0.3",
    author="jjmachan",
    author_email="jamesjithin97@gmail.com",
    description="Object Detection package for Aeye",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjmachan/objectdetection-aye",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
