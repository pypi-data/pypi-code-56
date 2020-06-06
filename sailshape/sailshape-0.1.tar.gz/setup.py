from distutils.core import setup
setup(
  name = 'sailshape',         # How you named your package folder (MyLib)
  packages = ['sailshape'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple package to compute the shape of a heavily tensioned sail in a two dimensional uniform flow',   # Give a short description about your library
  author = 'Gaston Maffei',                   # Type in your name
  author_email = 'gastonmaffei@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Popeyef5/sailshape',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Popeyef5/sailshape/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Physics', 'Flow', 'Sail'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'matplotlib',
          'scipy',
          'sympy',
      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)