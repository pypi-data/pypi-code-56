import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'src', 'pandas_save_profiler', '__init__.py'), encoding='utf-8') as f:
    init_lines = f.readlines()
    init_version = [x for x in init_lines if x.startswith('__version__')][0]
    init_version = init_version.split('=')[1].replace('"', '').replace("'", "").strip()

setup(
    name='pandas_save_profiler',
    license='MIT',
    description='Tools to evaluate pandas performance when saving dataframes in different file formats.',
    version=init_version,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David Montaner',
    author_email='david.montaner@gmail.com',
    url='https://github.com/dmontaner/pandas_save_profiler',
    packages=['pandas_save_profiler'],
    package_dir={'': 'src'},
    project_urls={
        'Source Code'  : 'https://github.com/dmontaner/pandas_save_profiler',
        'Documentation': 'https://github.com/dmontaner/pandas_save_profiler',
        'Issue Tracker': 'https://github.com/dmontaner/pandas_save_profiler/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    keywords=[
        'pandas',
        'save',
        'profile',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'humanize',
        'memory_profiler>=0.57.0',
        'pyarrow',
        'SQLAlchemy',
        'xlwt', 'xlrd', 'openpyxl',
    ],
)
