import setuptools

setuptools.setup(
    name="angem-girvel", # Replace with your own username
    version="0.0.3",
    author="girvel",
    author_email="widauka@yandex.ru",
    description='Analytic geometry library',
    url="https://github.com/girvel/angem",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['text-viewer-girvel']
)