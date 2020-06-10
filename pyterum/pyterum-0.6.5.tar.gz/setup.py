from distutils.core import setup

setup(
    name='pyterum',         # How you named your package folder (MyLib)
    packages=['pyterum'],   # Chose the same as "name"
    version='0.6.5',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    description='A Python client for interfacing with the Iterum framework for repeatable data science',
    author='Edser & Mark',                   # Type in your name
    author_email='',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/iterum-provenance/pyterum',
    # I explain this later on
    download_url='https://github.com/iterum-provenance/pyterum/archive/v0.6.5.tar.gz',
    keywords=['Iterum', 'Python Client', 'Framework', 'Provenance',
              'Data Science'],   # Keywords that define your package best
    install_requires=[],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
