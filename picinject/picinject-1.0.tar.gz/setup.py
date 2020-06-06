from setuptools import setup,find_packages

setup(
    name="picinject",
    version="1.0",
    description="With picinject you can simply hide files in pictures and extract them again when you need them",
    install_requires=["colorama"],
    python_requires=">=3.6.*",
    author="Lewin Sorg",
    author_email="developermind405@gmail.com",
    scripts=["src/picinject.py"],
    url="https://github.com/spezialcoder/PicInject",
    license="MIT"
)
