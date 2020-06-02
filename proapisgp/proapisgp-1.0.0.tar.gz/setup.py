from setuptools import setup

setup(name='proapisgp',
      version='1.0.0',
      description='ProAPIs Google Play API.',
      url='https://proapis.cloud',
      author='ProAPIs',
      author_email='sales@proapis.cloud',
      license='GPL3',
      packages=['proapisgp'],
      package_data={'proapisgp': ['device.properties']},
      install_requires=['cryptography>=2.2',
                        'protobuf>=3.5.2',
                        'requests'])
