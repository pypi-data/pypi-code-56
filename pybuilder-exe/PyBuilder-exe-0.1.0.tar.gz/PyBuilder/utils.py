# -*- coding: utf-8 -*-
# @Time    : 2020-04-17 14:24
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : utils.py

import os
import sys
import typing
import shutil
import fnmatch
import importlib

def path4package(package: str, src: str = None) -> str:
    """
    根据包名获取路径
    :param package: 包名
    :param src: 源码根路径
    :return:
    """
    for path in sys.path:
        if src and path.startswith(src):
            continue
        if os.path.isdir(os.path.join(path, package)):
            return os.path.join(path, package)
    raise Exception("not found package: '%s'" % package)

def remove_pycache4dir(tree: str):
    """
    移除`__pycache__`文件夹
    :param tree: 路径
    :return:
    """
    if not os.path.isdir(tree):
        return
    tree = os.path.abspath(tree)
    if os.path.dirname(tree) == '__pycache__':
        shutil.rmtree(tree)
        return
    for dn in os.listdir(tree):
        remove_pycache4dir(os.path.join(tree, dn))

def read_patter4file(file: str) -> typing.List[str]:
    """
    读取文件的匹配项
    :param file: 文件路径
    :return:
    """
    file = os.path.abspath(file)
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines_n = []
            for line in lines:
                line = line.strip()
                if len(line) > 0 and not line.startswith('#'):
                    lines_n.append(line.split(' ')[0])
            return lines_n
    except Exception:
        return []

def parse_patter(pats: typing.List[str]) -> typing.Tuple[typing.List[str], typing.List[str]]:
    """
    分析匹配项
    ========
    /xx/    # 只匹配根目录下文件夹
    xx/     # 匹配所有的文件夹
    /xx     # 只匹配根目录下文件
    xx      # 匹配所有的文件
    !xx     # 除xx之外
    =========
    /xx/    =>  xx + xx/**
    xx/     =>  xx + xx/** + **/xx + **/xx/**
    /xx     =>  xx
    xx      =>  xx + **/xx
    !xx     =>  除xx之外
    :param pats: 匹配项列表
    :return: 包含的匹配项，除此之外的匹配项
    """
    pats_includes = []
    pats_excludes = []
    for pat in pats:
        if pat.startswith('!'):
            pat = pat[1:]
            pats_n = pats_excludes
        else:
            pats_n = pats_includes
        pats_n.append(pat)
        if pat.endswith('/'):   # 文件夹：xx/
            if pat.startswith('/'):     # '/'开头，表示根目录下的文件
                # 根目录下的文件夹：/xx/ => xx or xx/**
                pats_n.append(pat[1:-1])
                pats_n.append(pat[1:] + '**')
            else:
                # xx/ => xx or xx/** or **/xx or **/xx/**
                pats_n.append(pat[:-1])
                pats_n.append(pat + '**')
                pats_n.append('**/' + pat[:-1])
                pats_n.append('**/' + pat + '**')
        else:
            if pat.startswith('/'):  # '/'开头，表示根目录下的文件
                # 根目录下的文件：/xx => xx
                pats_n.append(pat[1:])
            else:
                # xx => xx or **/xx
                pats_n.append('**/' + pat)
    return pats_includes, pats_excludes

def match(fn: str, pats: typing.List[str], pats_no: typing.List[str]) -> bool:
    """
    匹配
    :param fn: 目标
    :param pats: 包含的匹配项
    :param pats_no: 除此之外的匹配项
    :return:
    """
    def _match(pats_: typing.List[str]) -> bool:
        if not fn:
            return False
        for pat in pats_:
            if fnmatch.fnmatch(fn, pat):
                return True
        return False
    return _match(pats) and not _match(pats_no)

def copy_file(src: str, target: str):
    """
    复制文件
    :param src: 源文件
    :param target: 目录文件
    :return:
    """
    src = os.path.abspath(src)
    target = os.path.abspath(target)
    try:
        shutil.copy(src, target)
    except FileNotFoundError:
        mkdir_p(os.path.dirname(target))
        shutil.copy(src, target)

def mkdir_p(tree: str):
    """
    新建文件夹`mkdir -p`
    :param tree: 路径
    :return:
    """
    tree = os.path.abspath(tree)
    if os.path.isdir(tree):
        return
    try:
        os.mkdir(tree)
    except FileNotFoundError:
        mkdir_p(os.path.dirname(tree))
        os.mkdir(tree)

def import_module4file(file: str):
    """
    根据文件导入模块
    :param file: 文件路径
    :return:
    """
    file = os.path.abspath(file)
    if not os.path.exists(file):
        raise FileNotFoundError(file)
    module = None
    for m in sys.modules:
        try:
            if m.__file__ == file:
                module = m
                break
        except AttributeError:  # 内建模块没有__file__属性
            continue
    if module:
        return module
    file_dir = os.path.dirname(file)
    in_path = True
    if file_dir not in sys.path:
        sys.path.append(file_dir)
        in_path = False
    module_name = os.path.splitext(os.path.basename(file))[0]
    module = importlib.import_module(module_name)
    if not in_path:
        sys.path.remove(file_dir)
    return module
