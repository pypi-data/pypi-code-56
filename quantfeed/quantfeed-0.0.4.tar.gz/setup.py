import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quantfeed", # Replace with your own username
    version="0.0.4",
    author="hetao",
    license='MIT',
    author_email="22002499@qq.com",
    description="QuantBox Future Data Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://data.quantbox.cn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='quantbox futures tick bar datacenter',
    install_requires=[
        'requests',
        'pandas'
    ],    
    python_requires='>=3.7',
)