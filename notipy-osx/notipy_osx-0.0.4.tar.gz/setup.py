import setuptools

with open('../README.md') as readme_file:
  readme = readme_file.read()

setuptools.setup(
    name='notipy_osx',
    version='0.0.4',
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    install_requires=[
        'pyobjc-core',
        'AppKit',
        'Foundation'
    ],
    license='MIT',
    url='https://github.com/ninest/notipy_osx',
    long_description_content_type="text/markdown",
    description='Display native customizable Mac OS dialogs and notifications with ease',
    long_description=readme,
)
