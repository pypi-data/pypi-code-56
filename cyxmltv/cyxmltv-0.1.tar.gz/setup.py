from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='cyxmltv',
      version='0.1',
      entry_points={
          'console_scripts': ['cyxmltv=main:run']
      },
      description='Utility to create XML TV formatted document',
      long_description=readme(),
      author='Harry Papaxenopoulos',
      author_email='hpapaxen@gmail.com',
      packages=['cyxmltv'],
      keywords='cyprus xmltv plex cypriot epg rik1 rik',
      license='MIT',
      install_requires=[
          'lxml',
          'requests',
          'beautifulsoup4',
          'pytz'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
