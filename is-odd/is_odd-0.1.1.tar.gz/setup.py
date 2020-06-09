from setuptools import setup

setup(
     name='is_odd',
     version='0.1.1',
     author='Dat Nguyen, Nam Vu',
     author_email='datnguyen.it09@gmail.com, yvisvu@gmail.com',
     packages=['is_odd'],
     url='https://github.com/datnguye/is-odd',
     license='MIT',
     description='A package to check if a number is odd or not',
     long_description_content_type="text/markdown",
     long_description=open('README.md').read(),
     install_requires=[],
     python_requires='>=3.7.5'
)