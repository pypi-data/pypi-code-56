# -*- coding: utf-8 -*-
# @Time    : 2020-05-28 09:50
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : _hook.py

class _Hook(object):
    from .data import BuildData

    def __init__(self):
        """
        build hook 类
        """
        # build data将开始解析时
        self.hook_data = _Hook._hook_implement_n
        # 已解析出项目中excludes项时
        self.hook_excludes = _Hook._hook_implement
        # 已解析出项目中ignores项时
        self.hook_ignores = _Hook._hook_implement
        # 已解析出项目中的包路径项时
        self.hook_build_lib_path = _Hook._hook_implement
        # 已解析出项目中的资源文件时
        self.hook_build_data = _Hook._hook_implement
        # 已解析出项目中的隐藏导入项时
        self.hook_build_imports = _Hook._hook_implement
        # 将开始编译时
        self.hook_pre_compile = _Hook._hook_implement_n
        # 已编译完成时
        self.hook_compiled = _Hook._hook_implement_n
        # 将开始build时
        self.hook_pre_build = _Hook._hook_implement_n
        # 已build完成时
        self.hook_built = _Hook._hook_implement_n

    @staticmethod
    def _hook_implement(target, data: BuildData, *args, **kwargs):
        return target

    @staticmethod
    def _hook_implement_n(data: BuildData, *args, **kwargs):
        pass

    def start4file(self, file: str):
        from PyBuilder import utils
        module = utils.import_module4file(file)
        self.start4module(module)

    def start4module(self, module):
        for k in self.__dict__:
            if k.startswith('hook_'):
                try:
                    self.__setattr__(k, module.__getattribute__(k))
                except AttributeError:
                    continue

Hook = _Hook()

if __name__ == '__main__':
    print(Hook.__dict__)
    pass