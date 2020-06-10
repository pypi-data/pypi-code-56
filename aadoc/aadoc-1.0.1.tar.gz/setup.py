import setuptools

setuptools.setup(
    name='aadoc',
    version='1.0.1',
    author="Dilli Babu R",
    author_email="dillir07@outlook.com",
    description='A tool that automatically generates documentation from Automation Anywhere comments',
    long_description="",
    long_description_contect_type="text/markdown",
    url="https://dillir07.github.io/aadoc/",
    packages=['aadocmodule', 'aadocmodule.html_helpers_module',
              'aadocmodule.stylesheet_source_module', 'aadocmodule.tags_module'],
    entry_points={
        "console_scripts":['aadoc=aadocmodule.command_line:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
