from setuptools import setup, find_packages

setup(name='networktools',
      version='0.9.0',
      description='NetworkTools are some special functions to help with software developing',
      url='http://www.gitlab.com/dpineda/networktools',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPL3',
      install_requires=["termcolor","pytz", "ujson"],
      packages=['networktools'],
      package_dir={'networktools': 'networktools'},
      package_data={
          'networktools': ['../doc', '../docs', '../requeriments.txt']},
      zip_safe=False)
