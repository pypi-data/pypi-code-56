import distutils

from setuptools import setup
from setuptools.command.test import test


class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        test.finalize_options(self)
        self.ensure_string_list('pytest_args')
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import late because pytest is only required for testing
        import pytest

        exitcode = pytest.main(self.pytest_args)
        if exitcode:
            msg = 'pytest failed!'
            self.announce(msg, distutils.log.ERROR)
            raise distutils.errors.DistutilsError(msg)


setup(
    name='robosignatory',
    version='0.6.7',
    description='fedora-messaging consumer that automatically signs artifacts',
    author='Patrick Uiterwijk',
    author_email='puiterwijk@redhat.com',
    url='https://pagure.io/robosignatory/',
    license='gplv2+',
    install_requires=[
        "fedora_messaging",
        "psutil",
        "boto3",
        "six",
        "click",
        # Don't depend on koji here: https://bugzilla.redhat.com/show_bug.cgi?id=1537197
        #"koji",
    ],
    tests_require=[
        "pytest",
        "mock",
    ],
    packages=[
        'robosignatory',
    ],
    entry_points="""
    [console_scripts]
    robosignatory = robosignatory.cli:cli

    [robosignatory.signing.helpers]
    echo = robosignatory.utils:EchoHelper
    sigul = robosignatory.utils:SigulHelper
    """,
    cmdclass={
        'test': PyTest,
    },
)
