from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gaussian_binomial_distribution_calculation',
      version='1.0.2',
      description='Gaussian and Binomial distributions ',
      packages=['gaussian_binomial_distribution_calculation'],
      author = 'Paribesh Ranabhat',
      author_email = 'paribessh_sab@hotmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=['matplotlib'],
      python_requires='>=3.6',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
    ],
      zip_safe=False)