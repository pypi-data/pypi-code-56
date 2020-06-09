from setuptools import setup
from networktools.requeriments import read

requeriments = read()

setup(name='gnsocket',
      version='0.9.5',
      description='GPS Network Socket, with asyncio stream manager',
      url='https://gitlab.com/pineiden/gus',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPL3',
      install_requires=["networktools","basic_queuetools", "basic_logtools"],
      packages=['gnsocket'],
      include_package_data=True,      
      package_dir={'gnsocket': 'gnsocket'},      
      zip_safe=False)
