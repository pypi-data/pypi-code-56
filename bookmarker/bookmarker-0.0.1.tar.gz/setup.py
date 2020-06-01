import setuptools

setuptools.setup(
    name="bookmarker",
    version="0.0.1",
    description="Library for adding a bookmark",
    url="https://github.com/shuttl-tech/shuttl_workflows",
    author="Shuttl",
    author_email="swarnima.gupta@shuttl.com",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["Flask-SQLAlchemy", "SQLAlchemy", "pytz"],
    extras_require={"test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"]},
)
