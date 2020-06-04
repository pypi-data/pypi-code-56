import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bharathjinka09", # Replace with your own username
    version="1.0",
    author="JINKA RANGA BHARATH",
    author_email="bharathjinka09@gmail.com",
    description="Provide a Country code and postal code.It will generate a map in a html file based on these details.Used pgeocode and folium packages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/bharathjinka09/zipcode_to_map/',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)