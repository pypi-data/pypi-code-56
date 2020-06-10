from setuptools import setup, find_packages

'''
py_modules:只识别.py文件，其他文件不识别
可以自动添加README.rst和MANIFEST.in文件，但不能自动添加LICENSE.txt文件
packages=find_packages 让setup自动查找需要打包的子包
platforms=["all"] 支持所有平台使用
'''
setup(
    name='fileutil',
    version='1.0.4',
    description=r'''
        file union,file split by row/size/column,txt file transform to excel or excel file transform to txt and so on
    ''',
    long_description=open('README.rst', encoding='utf8').read(),
    platforms=["all"],
    author='Mr linle',
    author_email='linle861021@163.com',
    python_requires='>=3',
    license='MIT',
    # py_modules=['common', 'filesplit', 'fileunion', 'filetransform', 'parser'],
    packages=find_packages(),
    install_requires=[
        'cchardet',
        'pathlib',
        'pandas',
        'xlrd',
        'numpy',
        'xlsxwriter'
    ],
    url='https://github.com/lurkera/fileutil'
)
