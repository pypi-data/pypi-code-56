import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as req:
    requirements = list(filter(None, [x if 'github.com' not in x else None for x in req.read().split('\n')]))

with open('requirements.txt') as req:
    dependencies = list(filter(None, [x if 'github.com' in x else None for x in req.read().split('\n')]))

EXCLUDE_FROM_PACKAGES = ['docs', 'tests*', '*ipynb']

setuptools.setup(
    name="queue-metrics",
    version="0.0.1",
    author="jackdotwa",
    author_email="jacques@spatialedge.co.za",
    description="Simple approximate queue model metrics ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    install_requires=requirements,
    dependency_links=dependencies,
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
