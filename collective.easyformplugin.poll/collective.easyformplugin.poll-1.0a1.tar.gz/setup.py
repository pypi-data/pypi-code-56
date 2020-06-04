# -*- coding: utf-8 -*-
"""Installer for the collective.easyformplugin.poll package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.easyformplugin.poll',
    version='1.0a1',
    description="Poll support for EasyForm",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Oshane Bailey',
    author_email='oshane@alteroo.com',
    url='https://github.com/collective/collective.easyformplugin.poll',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.easyformplugin.poll',
        'Source': 'https://github.com/collective/collective.easyformplugin.poll',
        'Tracker': 'https://github.com/collective/collective.easyformplugin.poll/issues',
        # 'Documentation': 'https://collective.easyformplugin.poll.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.easyformplugin'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'collective.easyform',
        'Products.GenericSetup>=1.8.2',
        'plone.api>=1.8.4',
        'plone.app.dexterity',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.easyformplugin.poll.locales.update:update_locale
    """,
)
