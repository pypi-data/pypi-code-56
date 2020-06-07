import setuptools 
with open("README.rst", encoding='utf-8') as fh:
    long_description = fh.read()
    
    
setuptools.setup(name='distributions_study',
      version='1.6',
      description='Gaussian and Binomial distributions',
      packages=setuptools.find_packages(),
      zip_safe=False,
      classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Shivtej Shete",
      author_email="shivtej.shete@gmail.com",
      python_requires='>=3.6.3',
      license='MIT'
      )
