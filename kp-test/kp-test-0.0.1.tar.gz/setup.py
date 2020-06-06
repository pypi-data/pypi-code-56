from setuptools import setup

setup(
   name='kp-test',
   version='0.0.1',
   author='Karan Pathak',
   author_email='pathakkaran1994@gmail.com',
   packages=['kp-test'],
   url='http://pypi.python.org/pypi/kp-test/',
   license='LICENSE.txt',
   description='Test package',
   long_description=open('README.md').read(),
   install_requires=[
       "numpy",
   ],
)
