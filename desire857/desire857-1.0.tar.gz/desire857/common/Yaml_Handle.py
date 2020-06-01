# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 10:27
# @Author  : Desire
# @Email   : yangyin1106@163.com
# @Blog    : https://www.cnblogs.com/desireyang/
# @File    : Yaml_Handle.py
# @Software: PyCharm


import yaml


class YamlHandle(object):

    def __init__(self, conf_file):
        self.conf_file = conf_file

    def __load(self) -> dict:
        """
        读取yaml文件，获取全部数据
        :return: dict
        """
        with open(file=self.conf_file, encoding='utf8') as f:
            data = yaml.load(f, yaml.FullLoader)
        return data

    def get_data(self, node):
        """
        获取节点数据
        :param node: 节点名称
        :return: dict&str
        """
        return self.__load()[node]

    def write_yaml(self, data, mode='w'):
        """
        往yaml里面写入数据
        data：要写入的数据
        mode：写入方式： w，覆盖写入， a，追加写入
        将原数据读取出来，如果没有要加入的key，则创建一个，如果有，则执行key下面的数据修改
        """
        try:
            old_data = self.__load() or {}
            for data_key, data_value in data.items():
                if not old_data.get(data_key):
                    old_data.setdefault(data_key, {})
                for value_key, value_value in data_value.items():
                    old_data[data_key][value_key] = value_value
            with open(self.conf_file, mode, encoding="utf-8") as f:
                yaml.dump(old_data, f)
            return True
        except Exception as error:
            print(f'yaml文件写入失败，错误如下：\n{error}')
            return False
