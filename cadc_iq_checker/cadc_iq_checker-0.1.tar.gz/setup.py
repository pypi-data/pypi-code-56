from setuptools import setup, find_packages

dependencies = ['vos',
                'numpy',
                'astropy',
                'sompy',
                'keras']

setup(
    name='cadc_iq_checker',
    entry_points={'console_scripts': 'cadc_iq_checker = cadc_iq_checker.cli:main'},
    version='0.1',
    url='',
    license='MIT',
    author='JJ Kavelaars',
    install_requires=dependencies,
    package_data={'cadc_iq_checker': ['config/*', ]},
    packages=find_packages(exclude=['tests', ]),
    author_email='JJ.Kavelaars@nrc-cnrc.gc.ca',
    description='Image Quality Assessment AI'
)
