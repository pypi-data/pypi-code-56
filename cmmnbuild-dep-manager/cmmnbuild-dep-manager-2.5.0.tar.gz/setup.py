"""
setup.py for cmmnbuild-dep-manager.

For reference see
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
from pathlib import Path
from setuptools import setup, find_packages


HERE = Path(__file__).parent.absolute()
with (HERE / 'README.md').open('rt') as fh:
    LONG_DESCRIPTION = fh.read().strip()


REQUIREMENTS: dict = {
    'core': [
        'entrypoints',
        'JPype1>=0.6.1',
        'requests',
        'six',
    ],
    'test': [
        'pytest',
    ],
}


setup(
    name='cmmnbuild-dep-manager',
    description="Manages CERN's Java dependencies across multiple Python "
                "packages",
    maintainer='CERN Accelerating Python',
    maintainer_email='acc-py-support@cern.ch',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://gitlab.cern.ch/scripting-tools/cmmnbuild-dep-manager',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    install_requires=REQUIREMENTS['core'],
    extras_require={
        **REQUIREMENTS,
        # The 'dev' extra is the union of 'test' and 'doc', with an option
        # to have explicit development dependencies listed.
        'dev': [req
                for extra in ['dev', 'test', 'doc']
                for req in REQUIREMENTS.get(extra, [])],
        # The 'all' extra is the union of all requirements.
        'all': [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
    package_data={'cmmnbuild_dep_manager.resolver': ['gradle-wrapper.zip']},
    include_package_data=True,
    # cmmnbuild-dep-manager puts special files in the package directory, so it
    # cannot be installed as a zip.
    zip_safe=False
)
