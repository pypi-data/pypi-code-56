from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='mini_vk',
    version='0.1.3',
    packages=find_packages(),
    install_requires=['requests', ],
    url="https://github.com/SemenovAV/mini_vk",
    license='MIT',
    author='SemenovAV',
    author_email='7.on.off@gmail.com',
    description='Small wrapper over the VK API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
