from setuptools import setup, find_packages
setup(
      name = 'tello_binom',
      version = '1.0.1',
      py_modules=['tello_binom'],
      install_requires = [
          'opencv-python',
          'pillow',
          'pygame'
      ]
  )
