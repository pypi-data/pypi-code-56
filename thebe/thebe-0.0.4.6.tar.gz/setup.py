from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='thebe',
        version='0.0.4.6',
        description='Automatically runs and displays python code in browser.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author_email='hairyhenry@gmail.com',
        url='https://github.com/hotsoupisgood/Satyrn',
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            'flask',
            'flask_socketio',
            'pygments',
            'dill',
            'pypandoc',
            'jupyter_client',
            ],
        entry_points={
            'console_scripts': [
                'thebe = thebe.thebe:main',
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
        )
