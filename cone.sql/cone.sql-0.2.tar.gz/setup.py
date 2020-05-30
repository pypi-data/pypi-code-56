from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '0.2'
shortdesc = 'SQLAlchemy integration for cone.app'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])


class Test(test):

    def run_tests(self):
        from cone.sql import tests
        tests.run_tests()


setup(
    name='cone.sql',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='node pyramid cone web',
    author='Robert Niederreiter',
    author_email='dev@bluedynamics.com',
    url=u'https://github.com/bluedynamics/cone.sql',
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['cone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.sqlalchemy',
        'node.ext.ugm',
        'pyramid_tm',
        'pyramid_retry',
        'cone.app',
    ],
    extras_require=dict(test=['zope.testrunner']),
    tests_require=['zope.testrunner'],
    cmdclass=dict(test=Test),
    entry_points="""\
    [paste.filter_app_factory]
    session = cone.sql:make_app
    """
)
