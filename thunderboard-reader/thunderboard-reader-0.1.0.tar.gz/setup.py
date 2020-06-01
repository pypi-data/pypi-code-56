import setuptools
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thunderboard-reader", # Replace with your own username
    version="0.1.0",
    author="Lucas J. Koerner",
    author_email="koerner.lucas@stthomas.edu",
    # entry_points={'console_scripts': [
    #    CLI + ' = gdm.cli:main',
    #    'git-' + PLUGIN + ' = gdm.plugin:main',
    #]},
    scripts = ['tboard_read/tboard_read.py'],
    description="Reads data over the USB interface from the Silicon Labs Thunderboard Sense2",
    url="https://github.com/lucask07/thunderboard-reader/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
    license = 'MIT Licence',
    install_requires = ['pyserial', 'numpy', 'matplotlib',
                'appnope', 'pandas']
)
