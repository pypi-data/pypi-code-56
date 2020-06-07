import setuptools
from gitmanager.utils import get_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitmantool",
    version=str(get_version()),
    author='katmai',
    author_email='katmai.mobil@gmail.com',
    description='Console tool for manage projects on github/gitlab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/katmai1/gitmanager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'gm=gitmanager:main',
        ],
    },
    install_requires=[
        'docopt', 'pygithub', 'gitlab', 'pyyaml', 'colorama'
    ],
)
