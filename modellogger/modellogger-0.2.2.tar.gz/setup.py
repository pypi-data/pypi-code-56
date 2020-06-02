from setuptools import setup

setup(name='modellogger',
      version='0.2.2',
      url='https://github.com/SohamPathak/modellogger.github.io',
      author='SohamPathak',
      author_email='sohamkiit636@gmail.com',
      license='Apache License 2.0',
      packages=['modellogger'],
      zip_safe=True,
	description="Modelloger is a Python library for storing model's profile and rapid inter model comparision.",
      long_description=open("README.rst").read(),
	  install_requires=[
		"pandas",
		"dash",
            "plotly",
		"joblib",
		],

      )