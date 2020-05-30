from setuptools import setup
from setuptools.command.install import install
from os import getenv, getcwd

with open('requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.split('#', 1)[0].strip(' \t\n') for line in f
        ] if s != ''
    ]


class InstallWrapper(install):

    media_path = "media"
    static_path = "static"

    def run(self):
        super().run()
        self.static_path = getenv("STATIC_PATH", f"{getcwd()}/{self.static_path}")


setup(
    install_requires=install_reqs
)
