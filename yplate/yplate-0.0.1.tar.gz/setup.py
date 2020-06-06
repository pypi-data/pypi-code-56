from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

def readme():
	with open('README.md') as f:
		README = f.read()
	return README

setup( 
		name ='yplate', 
		version ='0.0.1', 
		author ='Deepraj Baidya', 
		author_email ='bdeeprajrkm1@gmail.com', 
		url ='https://github.com/deepraj1729/yplate', 
		description ='Plate Detection using YOLO v3 powered by OpenCV >=3.x ', 
		long_description = readme(), 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(), 
		entry_points ={ 
			'console_scripts': [ 
				'yplate = yplate.yplate:main'
			] 
		}, 
		classifiers =( 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		), 
		keywords ='Detect car/vehicle number plates with ease',
		include_package_data = True, 
		install_requires = requirements, 
		zip_safe = False
) 
