from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="relink",
      version="0.0.1",
      description="A client for https://rel.ink/ API",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Romain Ardiet",
      author_email="romardie@publicisgroupe.net",
      packages=["relink", "tests"],
      install_requires=["requests"],
      extras_require={
            "dev": ["requests-mock"],
      },
      license="Apache 2.0",
      classifiers=[
            "Development Status :: 5 - Production/Stable",

            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
            "Environment :: Console",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",

            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",

            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
      ])
