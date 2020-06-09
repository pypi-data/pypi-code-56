try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from pathlib import Path
import bashcalc

__author__ = "Anselm Hahn"
__email__ = "Anselm.Hahn@gmail.com"


def long_description():
    with open(Path("./README.md")) as f_1:
        readme = f_1.read()
    with open(Path("./CHANGES.md")) as f_2:
        changes = f_2.read()
    with open(Path("./TODO.md")) as f_3:
        todo = f_3.read()

    long_description = (
        f"{readme}\n\n"
        f"CHANGES\n"
        f"-------\n"
        f"{changes}\n"
        f"TODO\n"
        f"----\n"
        f"{todo}\n"
    )
    return long_description

setup(
    name="bashcalc",
    version=bashcalc.__version__,
    description="Instant calculating from the terminal into the terminal",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    packages=["bashcalc",],
    py_modules=[path.stem for path in Path(".").glob("bashcalc/*.py")],
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    url="https://github.com/Anselmoo/bashcalc",
    license="MIT",
    entry_points={
        "console_scripts": ["bashcalc = bashcalc.bashcalc:command_line_runner"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    keywords=["console", "terminal", "calculator", "data-science", "shell", "bash"],
    extras_require={"testing": ["pipenv"]},
)
