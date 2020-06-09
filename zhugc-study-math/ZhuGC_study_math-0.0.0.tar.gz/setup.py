from setuptools import setup, find_packages

setup(
    url='https://github.com/gzu300',
    author='zhu',
    author_email='zhuguanchen@me.com',
    name='ZhuGC_study_math',
    entry_points = {
        'console_scripts': ['calculate = pkg.Linear_Algebra:main',]
    },
    install_requires=['numpy'],
    packages=find_packages()
)