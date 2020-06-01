from distutils.core import setup
setup(
    name='ansible-nwd',
    packages=['ansible-nwd'],
    version='0.1',
    license='MIT',
    description='Ansible role automatic documentation',
    author='VASSEUR Laurent',
    author_email='mail.laurentvasseur@gmail.com',
    url='https://github.com/VasseurLaurent/ansible-nwd',
    # I explain this later on
    download_url='https://github.com/VasseurLaurent/ansible-nwd/archive/v0.1.tar.gz',
    keywords=['ansible', 'documentation', 'automation'],
    install_requires=[
        'ruamel.yaml',
        'ruamel.yaml.clib',
        'jinja2-time',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
    ],
)
