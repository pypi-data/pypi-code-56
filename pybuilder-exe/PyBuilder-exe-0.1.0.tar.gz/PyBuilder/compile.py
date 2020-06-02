# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 19:12
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : compile.py

import os
import shutil
import typing
from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext

def run(compile_dir: str, compile_files: typing.List[str]):
    """
    编译工程
    :param compile_dir: 编译文件夹路径
    :param compile_files: 需要编译的文件
    :return:
    """
    _compile(compile_files, compile_dir)

def _compile(compile_files: typing.List[str], compile_dir: str):
    build_tmp_dir = os.path.join(compile_dir, 'tmp')
    setup(
        ext_modules=cythonize(
            compile_files,
            compiler_directives=dict(
                always_allow_keywords=True,
                c_string_encoding='utf-8',
                language_level=3
            )
        ),
        cmdclass=dict(
            build_ext=build_ext
        ),
        script_args=["build_ext", "-b", compile_dir, "-t", build_tmp_dir]
    )
    shutil.rmtree(build_tmp_dir)
    # 处理过渡文件
    _handle_transition_files(compile_files=compile_files, compile_dir=compile_dir)

def _handle_transition_files(compile_files: typing.List[str], compile_dir: str):
    # 移除`build`文件夹中已编译的源码文件及其对应的`*.c`文件
    for f in compile_files:
        if os.path.isfile(f):
            os.remove(f)
        f_c = f.replace('.py', '.c')
        if os.path.isfile(f_c):
            os.remove(f_c)
    # 重命名`build`文件夹中的`*.so`文件
    for root, dirs, files in os.walk(compile_dir, topdown=True):
        for file_name in files:
            if file_name.endswith('.so'):
                file_name_fields = file_name.split('.')
                if len(file_name_fields) >= 3:
                    file_name_fields.pop(-2)
                    new_file_name = '.'.join(file_name_fields)
                    os.rename(os.path.join(root, file_name), os.path.join(root, new_file_name))

if __name__ == '__main__':
    pass