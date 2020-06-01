import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='chorder',
    version='0.0.5',
    author='Joshua Chang',
    author_email='chchang6@illinois.edu',
    description='A chord identifier and harmonizer for MIDI files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bit.ly/wallylay',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
