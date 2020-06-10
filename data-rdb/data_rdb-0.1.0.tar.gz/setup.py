from setuptools import setup, find_packages

setup(name='data_rdb',
      version='0.1.0',
      description='DataDBS for RethinkDB',
      url='http://www.gitlab.com/dpineda/data_rdb',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['data_rdb'],
      install_requires=['datadbs',"rethinkdb"],
      include_package_data=True,      
      package_dir={'data_rdb': 'data_rdb'},
      package_data={
          'data_rdb': ['../doc', '../docs', '../requeriments.txt', '../tests']},
      zip_safe=False)
