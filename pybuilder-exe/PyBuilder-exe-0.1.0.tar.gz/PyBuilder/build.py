# -*- coding: utf-8 -*-
# @Time    : 2020-04-03 15:14
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : build.py

import sys
import typing
import PyInstaller.__main__
sys.setrecursionlimit(50000)        # 修改默认递归深度

def run(name: str, target_file: str, build_dir: str, lib_dirs: typing.List[str] = [],
        data: typing.List[typing.Tuple[str, str]] = [], imports: typing.List[str] = [], single=False):
    """
    Src to exe
    :param name: 程序名
    :param target_file: 程序入口文件
    :param build_dir: `build`文件夹路径
    :param lib_dirs: 依赖包路径
    :param data: 程序内的资源文件信息，`(绝对路径, 相对路径)`
    :param imports: 程序内需手动导入的部分依赖包(`PyInstaller`未分析出来的依赖包)
    :param single: 如果`True`，则只生成一个执行文件(包含依赖文件)；否则便生成一个文件夹，包含依赖文件和执行文件(默认)
    :return:
    """
    args = [
        '--name=%s' % name,
        '--specpath=%s' % build_dir      # `.spec`文件的路径
    ]
    args.extend(['-p=%s' % d for d in lib_dirs])
    args.extend(['--add-data=%s:%s' % (abs_p, rel_p) for abs_p, rel_p in data])
    args.extend(['--hidden-import=%s' % p for p in imports])
    args.append('-F' if single else '-D')
    # args.append('--log-level=%s' % 'DEBUG')             # TRACE, DEBUG, INFO, WARN, ERROR (default: INFO).
    args.append(target_file)             # 目标文件
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    pass