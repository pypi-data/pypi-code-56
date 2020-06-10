import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='k_mxt_w3',
                 version='0.0.2',
                 description='k-mxt and k-mxt-w clustering algorithms',
                 author='Anastasia Stepanova',
                 author_email='stacey.stepanova@gmail.com',
                 url='https://github.com/stacy-s/k_mxt_w',
                 zip_safe=False,
                 include_package_data=True,
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 install_requires=['numpy', 'pandas', 'scipy'],
                 packages=['k_mxt_w3'],
                 python_requires=">=3.5",
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent",
                 ],
                 )
