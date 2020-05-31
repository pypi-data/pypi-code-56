from setuptools import setup

setup(
    name='atcli',
    version='0.11',
    packages=['atcli'],
    entry_points = {
      'console_scripts': [
          'atcli=atcli.__main__:main'
      ]
    },
    url='',
    license='',
    author='npraskins',
    author_email='',
    description='',
    python_requires='>=3.6'
)
