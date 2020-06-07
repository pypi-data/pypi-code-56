import setuptools

LONG_DESC = '''# googdiff: command-line diff tool, a wrapper of Google's diff-match-patch module.

See [the API doc of Google's diff-match-patch
module](https://github.com/google/diff-match-patch).

## Install googdiff with pip

```
pip install googdiff
```

## Usage

```
# Usage info
googdiff --help

# Show diffs in console mode:
googdiff file1 file2

# or:
googdiff -c file1 file2

# Show diffs in web browser:
googdiff -b file1 file2
```

## Git diff with googdiff

```
# in text mode:
git difftool -y --extcmd=googdiff

# or, in browser:
git difftool -y --extcmd='googdiff -b'
```
'''

setuptools.setup(
    name='googdiff',
    version='0.4.0',
    author='wixette',
    author_email='wixette@gmail.com',
    description='A wrapper of Google\'s diff-match-patch module.',
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    install_requires=[
        'console',
        'diff-match-patch'
    ],
    license='apache-2.0',
    packages=setuptools.find_packages(),
    url='https://github.com/wixette/googdiff',
    scripts=['googdiff'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
    python_requires='>=3.6',
)
