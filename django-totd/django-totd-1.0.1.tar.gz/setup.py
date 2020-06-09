import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-totd", # Replace with your own username
    version="1.0.1",
    author="Michael Hall",
    author_email="mhall119@gmail.com",
    description="Django app for adding a Tip of the Day to any page",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GetTogetherComm/totd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django>=2.0.12',
    ],
)