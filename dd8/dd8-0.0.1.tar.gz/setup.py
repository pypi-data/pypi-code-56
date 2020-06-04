import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
    
setuptools.setup(
        name='dd8',
        version='0.0.1',
        author='Dude and Dudette',
        author_email='yuanqing87@gmail.com',
        description='Utility Package for Data Science Projects',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Microsoft :: Windows'
        ],
        python_requires='>=3.6'
)