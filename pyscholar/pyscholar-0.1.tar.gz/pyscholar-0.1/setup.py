from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
     name='pyscholar',
     version='0.1',
     description='Convert tables from pandas to latex or markdown format.',
     long_description=long_description,
     long_description_content_type='text/markdown',
     url='https://github.com/pankajkarman/markdown-scholar',
     author='Pankaj Kumar',
     author_email='pankaj.kmr1990@gmail.com',
     license='MIT',
     py_modules=['pyscholar'],
     install_requires=[
     "pandas", 'pytablewriter'
     ],
     python_requires=">=3.6",
     setup_requires=['setuptools'],
)
