from setuptools import setup
from setuptools.command.sdist import sdist

class my_sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""

    def run(self):
        self.run_command('compile_catalog')
        # sdist is an old style class so super cannot be used.
        sdist.run(self)

setup(
    setup_requires = ["setuptools >= 39.2.0", "Babel"],
    cmdclass={'sdist': my_sdist}
)
