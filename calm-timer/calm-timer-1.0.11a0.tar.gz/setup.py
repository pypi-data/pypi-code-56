from setuptools import setup

setup(
    name='calm-timer',
    version='1.0.11-alpha',
    packages=['ct', 'ct.gui'],
    url='https://gitlab.com/SunyataZero/calm-timer',
    license='GPLv3',
    author='Tord Dellsén',
    author_email='tord.dellsen@gmail.com',
    description='A simple timer application with some calm sounds to choose from',
    install_requires=["PyQt5", "PyAudio"],
    include_package_data=True
)
# https://stackoverflow.com/questions/37311505/can-i-use-setup-py-to-pack-an-app-that-requires-pyqt5
# ***PLEASE NOTE***: if testing we may get "Could not find a version that satisfies the requirement"
#  since there's not any PyQt in test.pypi

