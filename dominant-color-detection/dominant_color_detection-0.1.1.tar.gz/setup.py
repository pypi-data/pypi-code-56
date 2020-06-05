# -*- encoding: utf-8 -*-
# ! python3

from distutils.core import setup

setup(
    name='dominant_color_detection',
    packages=['dominant_color_detection'],
    version='0.1.1',
    license='MIT',
    description='Detects dominant color of an image',
    author='Hynek Davídek',
    author_email='hynek.davidek@biano.com',
    keywords=['image', 'color', 'detection', 'dominant', 'kmeans'],
    install_requires=['numpy', 'Pillow', 'scikit-learn'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
