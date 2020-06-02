import setuptools

setuptools.setup(
    name="cron_processor",
    version="0.0.1",
    description="Library to setup cron_processor",
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
    install_requires=["pyshuttlis", "bookmarker"],
    extras_require={"test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"]},
)
