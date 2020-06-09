from setuptools import setup


setup(
    name='skcvideo',
    version='0.1.2',
    description='video utils',
    author='SkillCorner',
    author_email='timothe.collet@skillcorner.com',
    license='MIT',
    packages=[
        'skcvideo',
    ],
    install_requires=[
        'numpy>=1.12.0',
        'opencv-python>=4.1.1.26',
    ])
