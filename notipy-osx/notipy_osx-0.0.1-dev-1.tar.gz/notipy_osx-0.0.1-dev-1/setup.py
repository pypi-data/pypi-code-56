from distutils.core import setup

with open('../README.md') as readme_file:
  README = readme_file.read()

setup(
    name='notipy_osx',
    version='0.0.1-dev-1',
    packages=[],
    license='MIT',
    description='Display native customizable Mac OS dialogs and notifications with ease',
    long_description_content_type="text/markdown",
    long_description=README,
)
