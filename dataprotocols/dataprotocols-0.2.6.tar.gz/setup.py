from setuptools import setup, find_packages

setup(name='dataprotocols',
      version='0.2.6',
      description='DataProtocols is a set of classes that implement protocols for data acquisition',
      url='http://gitlab.csn.uchile.cl/dpineda/dataprotocols',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      install_requires=['Click','networktools', 'basic-logtools'],
      scripts=[
          'dataprotocols/gsof/test_gsof.py',
          'dataprotocols/eryo/test_eryo.py'          
      ],      
      entry_points={
        'console_scripts':["gsof = dataprotocols.gsof.test_gsof:run_gsof",
                          "eryo = dataprotocols.eryo.test_eryo:run_eryo"]
        },
      packages=find_packages(),
      include_package_data=True,
      license='MIT',
      zip_safe=False)
