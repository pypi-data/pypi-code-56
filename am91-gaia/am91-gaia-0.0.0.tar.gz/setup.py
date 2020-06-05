from setuptools import setup, find_namespace_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    'jinja2',
]

setup(
    name='am91-gaia',
    version='0.0.0',
    author='Alejandro Alonso Mayo',
    author_email='alejandroalonsomayo@gmail.com',
    description='Project generation',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/AlejandroAM91/gaia',
    download_url = 'https://github.com/AlejandroAM91/gaia/archive/v0.0.0.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=requirements,
    entry_points={
        'console_scripts': 'gaia = am91.gaia.cli:main',
    },
    package_dir={'': 'src'},
    packages=['am91.gaia', 'am91.gaia_template_base'],
    package_data={
        'am91.gaia_template_base': [
            'templates/*.jinja',
            'templates/.*.jinja',
            'templates/**/*.jinja'
        ]
    }
)
