from distutils.core import setup
setup(
  name = 'pysnowly',
  packages = ['pysnowly'],
  version = '0.1',
  license='MIT',
  description = 'Ilan Z., Elad S.',   # Give a short description about your library
  author = 'Ilan Z., Elad S.',                   # Type in your name
  author_email = 'info@snowly.io',      # Type in your E-Mail
  url = 'https://github.com/user/pysnowly',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/snowly-io/pysnowly/archive/v_01.tar.gz',
  keywords = ['Snowly Trigger'],
  install_requires=[            # I get to this in a second
          'snowflake-connector-python',
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)