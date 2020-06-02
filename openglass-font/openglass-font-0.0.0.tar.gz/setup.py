from distutils.core import setup
try:
    with open('README.md') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name = 'openglass-font',
    packages = ['ogfont'],
    version = '0.0.0',
    license='MIT',
    description = 'Python module for getting OpenGlass font data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Sam Sloniker',
    author_email = 'scoopgracie@gmail.com',
    url = 'https://github.com/openglass-project/',
    keywords = ['openglass', 'font'],
    install_requires=[
            ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
