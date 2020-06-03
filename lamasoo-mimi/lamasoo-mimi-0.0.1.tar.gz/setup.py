import setuptools

with open("src/README.md", "r") as fh:
    README = fh.read()

setuptools.setup(
    name="lamasoo-mimi",
    version="0.0.1",
    author="alireza khosravian",
    author_email="alirezakhosravian@lamasoo.com",
    description="Agency CRS Log Middleware",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://git.lamasoo.com",
    include_package_data=True,
    install_requires=['jdatetime',
                      'django_tables2',
                      'django-phonenumber-field',
                      'phonenumbers',
                      'kavenegar',
                      'django-cryptography',
                      'pyJWT'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.7',
)

