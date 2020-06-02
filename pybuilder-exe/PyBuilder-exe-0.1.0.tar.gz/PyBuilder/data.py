# -*- coding: utf-8 -*-
# @Time    : 2020-06-01 10:19
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : data.py

import os
import typing
import logging
from PyBuilder import utils
from .config import Config

class BuildData(object):
    def __init__(self):
        """
        build的数据构建类
        """
        self._config: Config = Config()
        # excludes
        self.excludes: typing.List[str] = []
        self._excludes: typing.List[str] = []
        self._excludes_no: typing.List[str] = []
        # ignores
        self.ignores: typing.List[str] = []
        self._ignores: typing.List[str] = []
        self._ignores_no: typing.List[str] = []
        # build_lib_path
        self.build_lib_path: typing.List[str] = []
        # build_data
        self.build_data: typing.List[typing.Tuple[str, str]] = []
        # build_imports
        self.build_imports: typing.List[str] = []

        self.compile_files: typing.List[str] = []
        self.include_files: typing.List[str] = []
        self.ignored_files: typing.List[str] = []

    @property
    def config(self):
        return self._config

    def parse(self, name, target_file='', src_dir='', build_dir='', hook_file='', excludes_file='',
              ignores_file='', single=False, no_compile=False):
        """
        解析数据
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
        c = self.config
        c.parse(name=name, target_file=target_file, src_dir=src_dir, build_dir=build_dir,
                hook_file=hook_file, excludes_file=excludes_file, ignores_file=ignores_file,
                single=single, no_compile=no_compile)
        from ._hook import Hook
        Hook.hook_data(self)
        # excludes
        self.excludes = Hook.hook_excludes(utils.read_patter4file(c.excludes_file), self)
        self._excludes, self._excludes_no = utils.parse_patter(self.excludes)
        # ignores
        self.ignores = utils.read_patter4file(c.ignores_file)
        if '__init__.py' not in self.ignores:
            self.ignores.insert(0, '__init__.py')               # `__init__.py`不应被编译
        self.ignores = Hook.hook_ignores(self.ignores, self)
        self._ignores, self._ignores_no = utils.parse_patter(self.ignores)
        # build_lib_path
        self.build_lib_path = [c.src_dir] if c.no_compile else [c.compile_dir, c.src_dir]
        self.build_lib_path = Hook.hook_build_lib_path(self.build_lib_path, self)
        # 分析源文件
        self._parse_src()
        # build_data
        self.build_data = Hook.hook_build_data(self.build_data, self)
        # build_imports
        self.build_imports = Hook.hook_build_imports(self.build_imports, self)

    def copy4compile(self):
        """
        将需要编译的源文件复制到编译目录
        :return:
        """
        def _copy4compile(files: typing.List[str]):
            for file in files:
                if os.path.exists(file):
                    # 复制源文件到编译目录
                    utils.copy_file(file, file.replace(self.config.src_dir, self.config.compile_dir))
                elif os.path.basename(file) == '__init__.py':
                    # 防止目录不存在
                    utils.mkdir_p(os.path.dirname(file))
                    # 新建`__init__.py`
                    file_c = file.replace(self.config.src_dir, self.config.compile_dir)
                    logging.info('create new empty file: %s' % file_c)
                    with open(file_c, 'a') as _:
                        pass
        _copy4compile(self.include_files)
        _copy4compile(self.ignored_files)

    def _parse_src(self):
        c = self.config
        tree = c.src_dir
        include_files = []  # 被包含的文件
        ignored_files = []  # 被忽略的文件
        # 解析并备份源码文件用于编译
        for root, dirs, files in os.walk(tree, topdown=True):
            root_rel = '' if root == tree else root.replace(tree + os.path.sep, '')  # 相对于源码的路径
            # 当前目录是否被排除
            if self._match_excludes(root_rel):
                continue
            # 当前目录是否被忽略
            if self._match_ignores(root_rel):
                ignored_files.append(root)
                continue
            for file_name in files:
                file_rel = os.path.join(root_rel, file_name)
                # 当前文件是否被排除
                if self._match_excludes(file_rel):
                    continue
                file = os.path.join(root, file_name)
                # 当前文件是否被忽略，只有.py文件才能编译，入口文件不能编译
                if self._match_ignores(file_rel) or \
                        (not c.no_compile and not file_name.endswith('.py')) or \
                        (not c.no_compile and file == c.target_src_path):
                    ignored_files.append(file)
                else:
                    include_files.append(file)
            if not c.no_compile:
                # 确保每个需要编译的目录下都有一个`__init__.py`
                init_file = os.path.join(root, '__init__.py')
                if root_rel and not os.path.isfile(init_file):
                    if self._match_ignores(os.path.join(root_rel, '__init__.py')):
                        ignored_files.append(init_file)
                    else:
                        include_files.append(init_file)
        # self.build_data
        # 目录：(root/xx/dir, xx/dir)
        # 文件：(root/xx/file, xx)
        for f in ignored_files:
            if os.path.basename(f) != '__init__.py':
                f = os.path.abspath(f)
                f_rel = f.replace(c.src_dir + os.path.sep, '')
                f_rel = f_rel if os.path.isdir(f) else (os.path.dirname(f_rel) or '.')
                self.build_data.append((f, f_rel))
        # self.build_imports
        def _add_imports4module(m):
            if m not in self.build_imports:
                self.build_imports.append(m)
            idx = m.rfind('.')
            if idx != -1:
                _add_imports4module(m[:idx])
        for f in include_files:
            if os.path.basename(f) != '__init__.py':
                f = f[:-3] if f.endswith('.py') else f
                mm = f.replace(c.src_dir + os.path.sep, '').replace(os.path.sep, '.')
                _add_imports4module(mm)
        if not c.no_compile:
            self.compile_files = [f.replace(c.src_dir, c.compile_dir) for f in include_files]
        self.include_files = include_files
        self.ignored_files = ignored_files

    def _match_excludes(self, fn: str) -> bool:
        return utils.match(fn, self._excludes, self._excludes_no)

    def _match_ignores(self, fn: str) -> bool:
        return utils.match(fn, self._ignores, self._ignores_no)

if __name__ == '__main__':
    pass