import setuptools

setuptools.setup(
    name="fuqichen",
    version="0.0.5",
    author="Qichen Fu",
    author_email="fuqichen1998@gmail.com",
    description="A custom deep learning lib",
    url="https://github.com/fuqichen1998/dllib",
    license='MIT',
    packages=['dllib'],
    install_requires=[
        'numpy',
        'torch',
        'matplotlib',
    ],
    zip_safe=False
)
