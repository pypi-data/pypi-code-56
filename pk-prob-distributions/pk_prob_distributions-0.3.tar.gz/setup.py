from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pk_prob_distributions',
      version='0.3',
      author='Alexander Romero',
      author_email="alexander.romerobiz@gmail.com",
      description='Gaussian and Binomial distributions',
      long_description_content_type="text/markdown",
      long_description=long_description,
      packages=['pk_prob_distributions'],
      zip_safe=False)
