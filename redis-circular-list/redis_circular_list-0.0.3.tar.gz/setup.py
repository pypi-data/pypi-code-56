import setuptools
import pathlib
import pkg_resources

# pipreqs ./redis_circular_list

# https://stackoverflow.com/a/59971469
with pathlib.Path('./redis_circular_list/requirements.txt').open() as requirements_txt:
	install_requires = [
		str(requirement)
		for requirement
		in pkg_resources.parse_requirements(requirements_txt)
	]

setuptools.setup(
	name="redis_circular_list",
	version="0.0.3",
	author="7435171",
	author_email="48723247842@protonmail.com",
	description="Redis Circular List",
	url="https://github.com/48723247842/RedisCirclularList",
	packages=setuptools.find_packages() ,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.8',
	install_requires=install_requires
)