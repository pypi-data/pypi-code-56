from setuptools import setup

def readme():
	with open('readme.md') as f:
		README = f.read()
		return README	
		
setup (
	name = 'Prep GMAT tool-emialex',
	version = '1.2.1',
	description = 'access questions relating to GMAT', 
	long_description= readme(),
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/emialex',
	author = 'emi alex',
	author_email = '',
	packages= ['GMAT_app'],
	package_data={'GMAT_app' : ['user.txt']},
	include_package_data= True,
	install_requires = ['requests'],
	entry_points={
        "console_scripts": [
            "run=GMAT_app.GMAT:main",
        ]
    },
)
	
	