from setuptools import find_packages, setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='ProtonPySDK',
      version='0.1.0',
      description='Proton SDK In Python (P+)',
	  long_description=README,
	  include_package_data=True,
	  long_description_content_type="text/markdown",
      packages=find_packages(),
	  install_requires=[],
      author='HanzHaxors',
	  author_email="hanzhaxors@gmail.com",
	  # license='MIT',
	  classifiers=[
		'Development Status :: 1 - Planning',
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'License :: Free To Use But Restricted'
	  ],
      zip_safe=False)
