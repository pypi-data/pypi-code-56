from setuptools import setup
setup(
    name="algorithm-question-fetcher",
    version="1.0.0",
    description="A python package that retrieves random number of algorithm questions specified by the user from toptal.com",
    url="https://github.com/startng/forward-randalgo-babayega",
    author="Kolapo Opeoluwa Olamidun",
    author_email="kolapoolamidun@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["algorithm_question_fetcher"],
    include_package_data=True,
    install_requires=["beautifulsoup4", "requests"],
    entry_points={
        "console_scripts": [
            "algorithm-question-fetcher=algorithm_question_fetcher.question_fetcher:main",]
    },
)