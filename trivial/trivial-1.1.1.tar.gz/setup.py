from setuptools import setup


def readme():
    with open("Readme.md") as f:
        readMe = f.read()
    return readMe


setup(
    name="trivial",
    version="1.1.1",
    description="A python package to display random trivia questions and answers",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/startngstartng/Forward-RandAlgo-Victory-Wekwa",
    author="Wekwa Victory Chiamaka",
    author_email="victorywekwa@gmail.com",
    packages=["RandAlgo"],
    include_package_data=True,
    install_requires=[
        "click", "requests"],
    entry_points={
        "console_scripts": [
            "Forward-RandAlgo-Victory-Wekwa=RandAlgo.Trail_Vail:get_started",
        ]
    },

)
