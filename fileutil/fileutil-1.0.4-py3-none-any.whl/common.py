import time

import cchardet
from pathlib import Path
import pandas as pd
import xlrd
from re import sub


def print_list_formating(print_string, step=4):
    '''
    将列表或字典格式化打印输出
    :param print_string: 列表或字典
    :param step: 打印列的数量
    :return: 无返回值
    '''
    print()
    if isinstance(print_string, list):
        print_string = [' ' + str(i + 1) + '、' + print_string[i] + ' ' for i in range(len(print_string))]
    elif isinstance(print_string, dict):
        print_string = [' ' + str(key) + ':' + str(value) + ' ' for key, value in print_string.items()]
    line_len = 0
    for i in range(0, step):
        max_len = 0
        for j in range(i, len(print_string), step):
            len_str = len(print_string[j].encode('gbk'))
            if max_len < len_str: max_len = len_str
        for j in range(i, len(print_string), step):
            len_str = len(print_string[j].encode('gbk'))
            print_string[j] = print_string[j] + ' ' * (max_len - len_str)
        line_len += max_len
    print('+' + '-' * line_len + '+')
    for i in range(0, len(print_string), step):
        list1 = print_string[i:i + step]
        s = ''.join(list1)
        slen = len(s.encode('gbk'))
        print('|' + s + ' ' * (line_len - slen) + '|')
    print('+' + '-' * line_len + '+')
    print()


def read_title(file_path, skip_row=0):
    '''
    读取csv文件的表头
    :param file_path: csv文件路径
    :param skip_row: 跳过行数，跳过行数后的第一行为表头位置
    :return: 返回表头列表
    '''
    title = pd.read_csv(file_path, skiprows=skip_row, nrows=0, header=0, encoding=file_encoding(file_path))
    title = list(title.columns)
    return title


def get_files(path, keys, all=False):
    '''
    根据输入的关键字搜索pth路径内的文件
    :param path: 搜索目录路径
    :param keys: 搜索的文件关键字，如果是多个关键字可以传入列表，如果只有一个关键字可以传入字符串
    :param all: 是否需要遍历其内部所有文件夹内的路径
    :return: 如果搜索到文件返回list，否则返回None
    '''

    result = []
    path = Path(path)
    if not path.exists():
        raise ValueError('输入的路径不存在')
    if isinstance(keys, str): keys = [keys]

    for key in keys:
        if all is True:
            result += [x for x in path.rglob('*' + key)]
        else:
            result += [x for x in path.glob('*' + key)]
    if not result:
        raise ValueError('未找到相关类型文件')
    return result


def get_all_dir(path):
    '''
    通过递归遍历pth目录内的所有子文件夹，返回Path类型list
    :param path:目录路径
    :return: 如果能到子目录则返回Path类型list（包含自身的路径），如果查询不到字目录，则如果输入的pth是路径则返回pth，如果pth不是路径
            则返回None
    '''
    result = []
    if path.is_dir():
        result.append(path)
    for _p in path.iterdir():
        if _p.is_dir():
            get_all_dir(_p)
    if len(result) > 0:
        return result


def file_encoding(pth):
    '''
    返回探测出的文件编码格式
    :param pth: 文件路径
    :return: 返回str类型文件编码格式
    '''
    with open(pth, 'rb') as f:
        msg = f.read()
    encode = cchardet.detect(msg)['encoding']
    if not encode:
        print('不能获得文件编码方式')
        raise ValueError
    return encode


def read_excel(pth):
    '''
    通过xlrd读取excel里的每个sheet，yield每个sheet
    :param pth: 文件路径
    :return: 返回sheet
    '''
    wb = xlrd.open_workbook(pth)
    for ws in wb.sheets():
        if ws.visibility == 0:
            if ws.nrows > 0 and ws.ncols > 0:
                yield ws


def replace_invalid_char(title):
    '''
    在windows中不合法的文件路径内的字符替换成下划线
    :param title: 原字符
    :return: 替换后的字符
    '''
    rstr = r"[\/\\\:\*\?\"\<\>\|]."  # '/ \ : * ? " < > |'
    new_title = sub(rstr, "_", title)  # 替换为下划线
    return new_title


def input_data(input_type='str', title='内容'):
    '''
    输入内容，并对返回值进行限定
    :param input_type: 对输入内容类型的限定
    :param title: 输入提示
    :return: 如果输入的类型符合限定则返回，否则继续输入
    '''
    while True:
        ipt = input(f'请输入{title}:')
        if ipt:
            try:
                return eval(input_type + f'("{ipt}")')
            except Exception as e:
                print(f'输入{title}错误，请重新输入')
