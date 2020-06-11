import setuptools

setuptools.setup(
    name='borisml',  
    version='0.0.2',
    author="Philipp Wirth",
    author_email="philipp@whattolabel.com",
    description="A deep learning package for self-supervised learning",
    entry_points={"console_scripts": [
        "boris-train = boris.cli.train_cli:entry",
        "boris-embed = boris.cli.embed_cli:entry",
        "boris-magic = boris.cli.boris_cli:entry"]},
    install_requires=[
        'torch==1.4.0',
        'tqdm==4.45.0',
        'pandas==1.0.3',
        'torchvision==0.5.0',
        'numpy==1.18.1',
        'hydra-core==0.11.3',
        'prefetch_generator==1.0.1',
        'pytorch_lightning==0.7.6',
    ],
    packages=[
        'boris',
        'boris.cli',
        'boris.data',
        'boris.embedding',
        'boris.loss',
        'boris.models',
        'boris.transforms'],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     include_package_data=True,
 )