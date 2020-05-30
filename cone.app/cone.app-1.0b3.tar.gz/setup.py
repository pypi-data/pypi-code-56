from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '1.0b3'
shortdesc = 'Web application stub'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])


class Test(test):

    def run_tests(self):
        from cone.app import tests
        tests.run_tests()


setup(
    name='cone.app',
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
    url=u'https://github.com/bluedynamics/cone.app',
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['cone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Chameleon',
        'node>=0.9.23',
        'node.ext.ugm>=0.9.9',
        'pyramid>=1.5',
        'pyramid_zcml',
        'pyramid_chameleon',
        'bdajax>=1.11',
        'cone.tile>0.999',  # XXX: >=1.0b1
        'yafowil>2.3.1',  # XXX: >=2.3.2
        'yafowil.webob',
        'yafowil.bootstrap',
        'repoze.workflow',
    ],
    extras_require=dict(
        lxml=[
            'lxml'
        ],
        yaml=[
            'yafowil.yaml'
        ],
        test=[
            'lxml',
            'yafowil.yaml',
            'zope.testrunner'
        ],
        docs=[
            'Sphinx',
            'sphinx_bootstrap_theme',
            'repoze.sphinx.autointerface'
        ],
    ),
    tests_require=[
        'lxml',
        'yafowil.yaml',
        'zope.testrunner'
    ],
    cmdclass=dict(test=Test),
    entry_points="""\
    [paste.app_factory]
    main = cone.app:main
    [paste.filter_app_factory]
    remote_addr = cone.app:make_remote_addr_middleware
    """
)
