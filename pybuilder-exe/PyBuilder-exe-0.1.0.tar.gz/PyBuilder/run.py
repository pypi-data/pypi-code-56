# -*- coding: utf-8 -*-
# @Time    : 2020-05-28 16:34
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : run.py

from ._hook import Hook as _Hook
from .config import default_config as _default_config
from .data import BuildData as _BuildData

def run4args(args):
    run(name=args.name, target_file=args.target_file, src_dir=args.src_dir, build_dir=args.build_dir,
        hook_file=args.hook_file, excludes_file=args.excludes_file, ignores_file=args.ignores_file,
        single=args.F, no_compile=args.no_compile)

def run(name, target_file='', src_dir='', build_dir='', hook_file='', excludes_file='',
        ignores_file='', single=_default_config.single, no_compile=_default_config.no_compile):
    """
    打包
    :param name: 打包后的程序名
    :param target_file: 入口文件相对于`src_dir`的相对路径
    :param src_dir: 源文件根目录路径，默认为运行环境的根目录路径
    :param build_dir: build目录路径，默认为与运行环境的根目录同级的`builder`目录
    :param hook_file: hook文件路径
    :param excludes_file: `excludes`文件路径
    :param ignores_file: `ignore`文件路径
    :param single: 是否build为单文件程序，默认为False
    :param no_compile: 是否不编译.py文件，默认为False
    :return:
    """
    build_data = _BuildData()
    build_data.parse(name=name, target_file=target_file, src_dir=src_dir, build_dir=build_dir,
                     hook_file=hook_file, excludes_file=excludes_file, ignores_file=ignores_file,
                     single=single, no_compile=no_compile)
    _run(build_data)

def _run(build_data: _BuildData):
    c = build_data
    # compile
    if not c.config.no_compile:
        from .compile import run as compile_run
        _Hook.hook_pre_compile(c)
        c.copy4compile()
        compile_run(c.config.compile_dir, c.compile_files)
        _Hook.hook_compiled(c)
    # build
    from .build import run as build_run
    _Hook.hook_pre_build(c)
    build_run(name=c.config.name, target_file=c.config.target_path, build_dir=c.config.build_dir,
              lib_dirs=c.build_lib_path, data=c.build_data, imports=c.build_imports, single=c.config.single)
    _Hook.hook_built(c)

if __name__ == '__main__':
    pass