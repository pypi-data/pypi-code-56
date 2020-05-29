import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="music-code",
    version="0.0.9",
    author="Wesley Laurence and Henry Franklin",
    author_email="wesleylaurencetech@gmail.com",
    description="Python library for creating music",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesleyLaurence",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'soundfile',
        'scipy',
        'sklearn',
        'datetime',
        'pyaudio',
        'wave',
        'mysql-connector-python',
    ]
)