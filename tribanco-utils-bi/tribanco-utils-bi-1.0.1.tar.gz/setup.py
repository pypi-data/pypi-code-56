import setuptools


setuptools.setup(
    name='tribanco-utils-bi',
    version='1.0.1',
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author='Herculano Cunha',
    author_email='herculanocm@outlook.com',
    description='Utilitario para rotinas BI Tribanco',
    keywords='bi dw sqlserver tools utils',
    install_requires=['pandas','pymssql'],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
