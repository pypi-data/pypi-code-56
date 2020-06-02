import setuptools
import pathlib
import pkg_resources

# pipreqs ./local_ip_finder

# https://stackoverflow.com/a/59971469
with pathlib.Path('./local_ip_finder/requirements.txt').open() as requirements_txt:
	install_requires = [
		str(requirement)
		for requirement
		in pkg_resources.parse_requirements(requirements_txt)
	]

setuptools.setup(
	name="local_ip_finder",
	version="0.0.1",
	author="7435171",
	author_email="48723247842@protonmail.com",
	description="Local IP Finder",
	url="https://github.com/48723247842/LocalIPFinder",
	packages=setuptools.find_packages() ,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.8',
	install_requires=install_requires
)