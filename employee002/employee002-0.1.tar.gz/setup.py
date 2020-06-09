from setuptools import setup

setup(name='employee002',   ## this is the name when you pip install employee001, as project employee001 0.1
      version='0.1',        ## this is the version
      description='employee_name',
      packages=['employee_package'],    ## this is the name of package you can find in your local path after you pip install employee001
      zip_safe=False)


