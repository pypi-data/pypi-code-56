import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="yoohoo",
	version="0.0.3",
	author="Francois Campbell",
	author_email="campbellfd@gmail.com",
	description="Test Pip package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/LeFrank/pip_yoohoo.git",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	],
	python_requires=">=2.1",
)