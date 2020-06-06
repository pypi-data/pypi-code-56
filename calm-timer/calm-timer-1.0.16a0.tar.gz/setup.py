from setuptools import setup

LONG_DESCRIPTION_STR = "Calm Timer is a simple timer application with some calm sounds to choose from. It is build using PyQt for the GUI and pydub is used for playing audio files"

setup(
    name='calm-timer',
    version='1.0.16-alpha',
    packages=['ct', 'ct.gui'],
    url='https://gitlab.com/SunyataZero/calm-timer',
    license='GPLv3',
    author='Tord Dellsén',
    author_email='tord.dellsen@gmail.com',
    description='A simple timer application with some calm sounds to choose from',
    install_requires=["PyQt5", "pydub"],
    include_package_data=True,
    entry_points={"console_scripts": ["calm-timer=ct.__main__:main"]},
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION_STR,
    python_requires='>=3.0.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
# https://stackoverflow.com/questions/37311505/can-i-use-setup-py-to-pack-an-app-that-requires-pyqt5
# ***PLEASE NOTE***: if testing we may get "Could not find a version that satisfies the requirement"
#  since there's not any PyQt in test.pypi

