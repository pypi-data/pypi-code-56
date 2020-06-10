import setuptools

with open("PypiReadme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-satchmo",
    version="0.0.1",
    author="KALAMAR",
    author_email="entreprise.kalamar@gmail.com",
    description="A Django Satchmo app maintained .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hermann.kass/django-satchmo",
    packages=setuptools.find_packages(),
    install_requires=[
        'Django>=2.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)