from glob import glob
import os
from setuptools import setup
from setuptools.command.install import install
from os import getenv, getcwd

# __pkgname__ = "./"

with open('requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.split('#', 1)[0].strip(' \t\n') for line in f
        ] if s != ''
    ]

# data_files = []
#
# start_point = os.path.join(__pkgname__, 'static')
# for root, dirs, files in os.walk(start_point):
#     root_files = [os.path.join(root, i) for i in files]
#     data_files.append((root, root_files))
#
# start_point = os.path.join(__pkgname__, 'media')
# for root, dirs, files in os.walk(start_point):
#     root_files = [os.path.join(root, i) for i in files]
#     data_files.append((root, root_files))
#
# start_point = os.path.join(__pkgname__, 'doc')
# for root, dirs, files in os.walk(start_point):
#     root_files = [os.path.join(root, i) for i in files]
#     data_files.append((root, root_files))
#
# start_point = os.path.join(__pkgname__, 'templates')
# for root, dirs, files in os.walk(start_point):
#     root_files = [os.path.join(root, i) for i in files]
#     data_files.append((root, root_files))
#
# start_point = os.path.join(__pkgname__, 'logos')
# for root, dirs, files in os.walk(start_point):
#     root_files = [os.path.join(root, i) for i in files]
#     data_files.append((root, root_files))


class InstallWrapper(install):
    media_path = "media"
    static_path = "static"

    def run(self):
        super().run()
        self.static_path = getenv("STATIC_PATH", f"{getcwd()}/{self.static_path}")


setup(
    packages=[
        'api',
        'core',
        'db',
        'editorjs',
        'web',
    ],
    install_requires=install_reqs,
    include_package_data=True,
    setup_requires=['wheel'],
)
