import setuptools
import os

# LONG_DESCRIPTION_STR = ""
DESCRIPTION_STR = 'A productivity and life organizing application where data is stored as text files and directories'
long_description_str = ""

this_dir_abs_path_str = os.path.dirname(os.path.abspath(__file__))
readme_abs_path_str = os.path.join(this_dir_abs_path_str, "README.md")

try:
    with open(readme_abs_path_str, "r") as file:
        long_description_str = '\n' + file.read()
except FileNotFoundError:
    long_description_str = DESCRIPTION_STR

setuptools.setup(
    name='kammanta',
    version='1.0.9-alpha',
    packages=['kammanta', 'kammanta.gui', 'kammanta.widgets'],
    url='https://gitlab.com/SunyataZero/kammanta',
    license='GPLv3',
    author='Tord Dellsén',
    author_email='tord.dellsen@gmail.com',
    install_requires=["PyQt5"],
    include_package_data=True,
    description=DESCRIPTION_STR,
    long_description_content_type='text/markdown',
    long_description=long_description_str,
    python_requires=">=3.8.0",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Other/Nonlisted Topic',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop'
    ],
    entry_points={"console_scripts": ["kammanta=kammanta.__main__:main"]}
)

# Full list of classifiers here: https://pypi.org/classifiers/

# This doesn't seem to be needed under install_requires: "PyQt5-sip". Unknown why

# TODO: Packages: Merging GUI and widgets? Have GUI at all?

# TODO: Other types of entry points besides console_scripts? Search terms: entry_points console_scripts setup.py

# TODO: include screenshots in README.md file --- setup.py manifest file include keep directory
# https://stackoverflow.com/questions/35039043/how-can-images-be-added-to-python-package-index-documentation

# TODO: Single-sourcing the version:
# https://packaging.python.org/guides/single-sourcing-package-version/
