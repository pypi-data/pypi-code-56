
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'DjangoMpesa',
    version = '2.0',
    packages = ['mpesaApp'],
    include_package_data = True,
    license = 'BSD License',
    description = 'A simple Django app for integrating mpesa stk push payment to your django site.',
    long_description = README,
    url = 'http://www.techtenant.co.ke/',
    author = 'Oronz',
    keywords = ['MPESA', 'Django', 'Djangompesa'],   # Keywords that define your package best

    author_email = 'brianoroni6@gmail.com',
    classifiers =[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires= '>=3.8',
    install_requires=[
       'celery==4.3.0',
       'kombu==4.6.8',
       'credis==3.5.2',
       'requests==2.21.0',
       'django-celery-beat==1.1.1',

    ],

)
