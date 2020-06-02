from distutils.core import setup
setup(
  name = 'Aggdirect-util',         # How you named your package folder (MyLib)
  packages = ['Aggdirect_util'],
  version = '0.2',
  description = 'Util functions',
  author = 'Anupam Basu',
  author_email = '',
  url = '',   # Provide either the link to your github or to your website
  keywords = ['UTIL', 'AGGDIRECT'],   # Keywords that define your package best

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
