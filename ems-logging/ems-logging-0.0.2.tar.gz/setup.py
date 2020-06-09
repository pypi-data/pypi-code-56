from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='ems-logging',
    author="Jesper Halkjær Jensen",
    author_email="gedemagt@gmail.com",
    description="Common logging for EMS projects",
    version='0.0.2',
    url='https://github.com/',
    packages=['emslogging'],
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires='>=2.7'
)
