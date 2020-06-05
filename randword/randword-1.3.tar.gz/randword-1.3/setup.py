from setuptools import setup


setup(
    name='randword',
    description='A Python package for generation random English words',
    keywords=['generation', 'word', 'random', 'english'],
    version='1.3',

    author='Artyom Bezmenov (8nhuman)',
    author_email='artem.bezmenov02@gmail.com',
    license='MIT',

    #url='https://github.com/8nhuman8/rand-word',
    #download_url='https://github.com/8nhuman8/rand-word/archive/0.2.tar.gz',

    include_package_data=True,
    package_data={'randword': ['words/*.txt']},

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ]
)
