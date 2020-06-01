from setuptools import setup


def readme():
	with open("readme.md") as f:
		return f.read()


setup(
	name = "py-pesapal",
	author = "M69k65y",
	description = "PesaPal integration made easy",
	license = "MIT",
	url = "https://github.com/M69k65y/py-pesapal",
	version = "0.1.0",
	packages = ["py_pesapal"],
	install_requires = [
		"requests>=2.22.0"
		"requests_oauthlib>=1.3.0"
	],
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Framework :: Flask",
		"Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
		"Natural Language :: English",
        "Programming Language :: Python :: 3"
	],
	keywords = "pesapal flask python",
	long_description = readme(),
	long_description_content_type = "text/markdown",
	zip_safe = False
)