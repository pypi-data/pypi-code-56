import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testcases_executor",
    version="1.0.0",
    author="JBthePenguin",
    author_email="jbthepenguin@netcourrier.com",
    description="Executor of unittest.TestCase subclasses ordered by groups.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBthePenguin/TestCasesExecutor",
    packages=setuptools.find_packages(),
    package_data={'testcases_executor': ['tc_reporter/templates/*.html']},
    include_package_data=True,
    install_requires=['jinja2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
