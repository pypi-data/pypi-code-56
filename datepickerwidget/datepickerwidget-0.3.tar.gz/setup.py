from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'datepickerwidget',         # How you named your package folder (MyLib)
  packages = ['datepickerwidget'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Datepicker for django 2.1',   # Give a short description about your library
  author = 'Bernardo',                   # Type in your name
  author_email = 'b.vieira.rocha@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/upwardweb/datetimewidget.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Django', 'Python', 'Bootstrap'],   # Keywords that define your package best

  include_package_data=True,
  install_requires = ['django','pytz'],
  classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "License :: OSI Approved :: BSD License",
        'Topic :: Software Development :: Libraries :: Python Modules ',
        ],
  zip_safe=False,
)
