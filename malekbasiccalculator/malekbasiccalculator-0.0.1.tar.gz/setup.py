from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='malekbasiccalculator',
  version='0.0.1',
  description='A very basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Malek Jaouadi',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[
      'click==7.1.2',
      'Flask==1.1.2',
      'itsdangerous==1.1.0',
      'Jinja2==2.11.2',
      'MarkupSafe==1.1.1',
      'pkg-resources==0.0.0',
      'Werkzeug==1.0.1'
  ] 
)