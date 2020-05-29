from setuptools import setup, find_packages

with open("README.md", 'r') as file:
    long_description = file.read()


setup(
    name = 'RandAlgo',
    version ='1.0.0',
    author = 'Munachimso Ike',
    author_email = 'ikemunachii@gmail.com',
    description = 'A package that displays random algorithm questions',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    py_modules = ['RandAlgo'],
    classifiers = [
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    packages = find_packages(),
    python_requires = '>= 3.6',
    install_requires = ['requests'],
    entry_points = {
        'console_scripts' : [
            'RandAlgo = Randlgo:__main__',
        ]

    }

)