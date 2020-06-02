# -*- coding: utf-8 -*-
# @Time    : 2020-05-28 14:29
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : config.py

import os
import logging

class Config(object):
    def __init__(self):
        """
        build的基础配置类
        """
        self.name: str = 'main'                                                         # 程序名
        self._target_file: str = 'main.py'                                              # 程序入口文件名
        self._src_dir: str = os.getcwd()                                                # 程序源码文件夹路径
        self._build_dir: str = os.path.join(os.path.dirname(self.src_dir), 'builder')   # build文件夹路径
        self._hook_file: str = ''                                                       # hook文件路径
        self.excludes_file: str = os.path.join(os.path.dirname(__file__), 'excludes')   # excludes文件路径
        self.ignores_file: str = os.path.join(os.path.dirname(__file__), 'ignores')     # ignores文件路径
        self.single: bool = False                                                       # 是否build为单文件程序
        self.no_compile: bool = False                                                   # 是否不需要编译

        self.compile_dir: str = os.path.join(self.build_dir, 'compile')                 # 编译文件夹

    @property
    def target_file(self) -> str:
        return self._target_file

    @target_file.setter
    def target_file(self, n: str):
        self._target_file = n
        if not self.name:
            self.name = os.path.splitext(n)[0]

    @property
    def target_path(self) -> str:
        return os.path.join(self.src_dir if self.no_compile else self.compile_dir, self.target_file)

    @property
    def target_src_path(self) -> str:
        return os.path.join(self.src_dir, self.target_file)

    @property
    def src_dir(self):
        return self._src_dir

    @src_dir.setter
    def src_dir(self, n: str):
        self._src_dir = n
        if not os.path.isdir(n):
            logging.error("PyBuilder directory doesn't exists: %s" % n)
            raise Exception("PyBuilder directory doesn't exists: %s" % n)

    @property
    def build_dir(self):
        return self._build_dir
    
    @build_dir.setter
    def build_dir(self, n: str):
        self._build_dir = n
        self.compile_dir = os.path.join(n, 'compile')

    @property
    def hook_file(self):
        return self._hook_file

    @hook_file.setter
    def hook_file(self, n: str):
        if n:
            self._hook_file = n
            # Hook
            from ._hook import Hook
            Hook.start4file(n)

    def parse(self, name, target_file='', src_dir='', build_dir='',
              hook_file='', excludes_file='', ignores_file='', single=False, no_compile=False):
        """
        解析基础配置
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
        self.name = name or self.name
        self.target_file = target_file or self.target_file
        self.src_dir = src_dir or self.src_dir
        self.build_dir = build_dir or self.build_dir
        self.hook_file = hook_file or self.hook_file
        self.excludes_file = excludes_file or self.excludes_file
        self.ignores_file = ignores_file or self.ignores_file
        self.single = single
        self.no_compile = no_compile

default_config = Config()

if __name__ == '__main__':
    pass