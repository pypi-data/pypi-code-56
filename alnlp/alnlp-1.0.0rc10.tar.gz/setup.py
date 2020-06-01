from setuptools import find_packages, setup

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release

# version.py defines the VERSION and VERSION_SHORT variables.
# We use exec here so we don't import allennlp whilst setting up.
VERSION = {}
with open("alnlp/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name="alnlp",
    version=VERSION["VERSION"],
    description="NLP metrics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="nlp metrics",
    url="https://github.com/allenai/allennlp",
    # The trademark for AllenAI should not be used
    # author="Allen Institute for Artificial Intelligence",
    # author_email="allennlp@allenai.org",
    license="Apache",
    packages=['alnlp'],
    install_requires=[
        "torch",
    ],
    include_package_data=False,
    python_requires=">=3.6",
    zip_safe=True,
)
