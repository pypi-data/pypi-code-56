import setuptools

setuptools.setup(
	name="viziocontroller",
	version="0.0.2",
	author="7435171",
	author_email="48723247842@protonmail.com",
	description="Vizio Controller",
	url="https://github.com/48723247842/VizioController",
	packages=setuptools.find_packages(include=['viziocontroller', 'viziocontroller.*']) ,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)

install_requires = [
	'sys' ,
	'os' ,
	'subprocess' ,
	'socket' ,
	'netifaces' ,
	'platform' ,
	'requests' ,
	'json' ,
	'warnings' ,
	'pprint' ,
]
