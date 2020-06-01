from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='nummer_games',
      version='0.2',
      description='Guess random numbers and prime numbers',
      packages=['nummer_games'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Akande Imisioluwa',
      author_email='imizezek84@gmail.com',
      url='https://github.com/imisi-akande/number-game',
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      python_requires='>=3.6',
    )