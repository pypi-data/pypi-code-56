import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-blog-comments", # Replace with your own username
    version="1.0.0",
    author="Naman Tamrakar",
    author_email="namantam1@gmail.com",
    description="A django app which help in implementing comments in your posts model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/namantam1/django-blog-comments",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)