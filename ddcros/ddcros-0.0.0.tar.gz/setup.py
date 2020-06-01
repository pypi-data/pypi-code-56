import setuptools
import ddcros
with open("describe.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
NAME = ddcros.NAME
VERSION = ddcros.__version__


PACKAGES = setuptools.find_packages()

setuptools.setup(
    name=NAME,
    version=VERSION,
    description='  ',
    long_description=long_description,
    author='fastbiubiu',
    author_email='fastbiubiu@163.com',
    url='https://github.com/NocoldBob/robot',
    # package_dir=PACKAGE_DIR,
    include_package_data=True,
    install_requires=["bottle",  "flask"],
    packages=PACKAGES,
    platforms='Linux',
    classifiers=[
        "Topic :: System :: Operating System Kernels :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",

    ],
    python_requires='>=3',
)
