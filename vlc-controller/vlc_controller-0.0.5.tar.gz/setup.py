import setuptools
import pathlib
import pkg_resources

# pipreqs ./vlc_controller

# https://stackoverflow.com/a/59971469
with pathlib.Path('./vlc_controller/requirements.txt').open() as requirements_txt:
	install_requires = [
		str(requirement)
		for requirement
		in pkg_resources.parse_requirements(requirements_txt)
	]

setuptools.setup(
	name="vlc_controller",
	version="0.0.5",
	author="7435171",
	author_email="48723247842@protonmail.com",
	description="VLC Controller",
	url="https://github.com/48723247842/VLCController",
	packages=setuptools.find_packages() ,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.8',
	install_requires=install_requires
)