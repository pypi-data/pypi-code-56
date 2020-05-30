from setuptools import setup, Extension
from Cython.Build import cythonize


with open("README.md", "r") as file:
    long_description = file.read()

dev_status = {
    "Alpha": "Development Status :: 3 - Alpha",
    "Beta": "Development Status :: 4 - Beta",
    "Pro": "Development Status :: 5 - Production/Stable",
    "Mature": "Development Status :: 6 - Mature",
}

setup(
    name="KnuthB",
    ext_modules=cythonize(
        Extension(
            name="KnuthB",
            sources=["KnuthB.pyx"],
            language=["c++"],
            extra_compile_args=["-std=c++17"],

        ),
        compiler_directives={
            'embedsignature': True,
            'language_level': 3,
        },
    ),
    author="Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    version="0.0.1",
    description="Knuth B Shuffle Algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        dev_status["Alpha"],
    ],
    keywords=["Shuffle", "Knuth B Algorithm"],
    python_requires='>=3.6',
)
