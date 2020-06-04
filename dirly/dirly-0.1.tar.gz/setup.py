from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='dirly',
      version='0.1',
      description='Quickly map your function to every file in a directory (verb: to dirl).',
      url='https://github.com/SharifElfouly/dirly',
      author='Sharif Elfouly',
      author_email='selfouly@gmail.com',
      license='MIT',
      packages=['dirly'],
      install_requires=['numpy', 'pillow'])
