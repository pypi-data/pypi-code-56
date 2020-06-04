# -*- coding: utf-8 -*-
# @Time: 2020/6/3 0003
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:
import os
import sys


def __init_project_path():
    """
        获取项目根路径
        PROJECTPATH未配置,默认为当前执行路径src所在目录，依据最近匹配原则。
        若要更改项目路径,在import aixm前添加以下代码
        import os
        os.environ["PROJECTPATH"]=projectpath
        或者终端执行
        export PROJECTPATH=projectpath
    :return:
    """
    project_path = os.getenv('PROJECTPATH')
    if project_path is not None:
        return project_path
    file_path = os.path.realpath(sys.argv[0])
    split_dir = file_path.split(os.sep)
    split_dir.insert(0, split_dir[0] + os.sep)
    if "src" in split_dir:
        for i in range(0, len(split_dir)):
            if split_dir[-i] == "src":
                return os.path.join(*split_dir[:-i])
        # raise Exception("PROJECT PATH NOT CONFIG")
    else:
        return os.path.join(*split_dir[:-1])


__project_path = os.path.join(__init_project_path(), 'src')


def relative_project_path(*args):
    return os.path.join(__project_path, *args)


log_cfg_path = relative_project_path('cfg', 'log_config.ini')
cfg_path = relative_project_path('cfg', 'config.ini')

if __name__ == '__main__':
    print(log_cfg_path)
