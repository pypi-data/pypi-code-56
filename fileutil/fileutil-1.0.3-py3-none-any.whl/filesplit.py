import csv
import re
from math import ceil
from pathlib import Path

import numpy as np
import pandas as pd

from .common import file_encoding, replace_invalid_char, input_data
from . import EXCEL_TYPE, TXT_TYPE
from . import common
from .filetransform import excel_to_csv
from .parser import split_file

# pd.set_option('max_columns', 1000, 'max_rows', 100, 'expand_frame_repr', False)


def split_by_row(save_path, file_path, row_num, skip_row=0, need_title=False, **kwargs):
    save_path, file_path = Path(save_path), Path(file_path)
    if file_path.suffix in EXCEL_TYPE:
        file_path = excel_to_csv(file_path.parent, file_path)
        keep_file = False
    else:
        file_path = [file_path]
        keep_file = True
    result = []
    kwargs.update(keep_file=keep_file, skip_row=skip_row, need_title=need_title, row_num=row_num)
    for file in file_path:
        result.append(split_file(save_path, file, engine='row', **kwargs))
    return result


def split_by_size(save_path, file_path, size, skip_row=0, need_title=False, **kwargs):
    save_path, file_path = Path(save_path), Path(file_path)
    keep_file = True
    if file_path.suffix not in TXT_TYPE:
        file_path = excel_to_csv(file_path.parent, file_path)
        keep_file = False
    else:
        file_path = [file_path]
    result = []
    kwargs.update(keep_file=keep_file, skip_row=skip_row, need_title=need_title, size=size)
    for file in file_path:
        result.append(split_file(save_path, file, engine='size', **kwargs))
    return result


def split_by_column(save_path, file_path, column, skip_row=0, **kwargs):
    save_path, file_path = Path(save_path), Path(file_path)
    keep_file = True
    if file_path.suffix not in TXT_TYPE:
        file_path = excel_to_csv(file_path.parent, file_path)
        keep_file = False
    else:
        file_path = [file_path]
    result = []
    kwargs.update(skip_row=skip_row, keep_file=keep_file, column=column)
    for file in file_path:
        result.append(split_file(save_path, file, engine='column', **kwargs))
    return result


def mml_split_file(file_path):
    '''
    对mml文件进行分割，主要考虑因素：
    1、如果是excel类型文件，则按照sheet转换为csv文件
    2、如果第一行不是表头，则需要跳过n行，直到表头出现
    3、mml脚本基站数量限制1000个以内
    4、mml脚本大小限制5M以内
    :param file_path: mml文件路径
    :return: None
    '''
    skip_row = input_data('int', f'mml文件跳过行数')
    site_num = input_data('int', f'mml文件基站数量')
    file_size = input_data('int', f'mml文件大小(mb)') * 1024 * 1024
    file_path = Path(file_path)
    keep_file = True  # 最后需要将excel转csv的文件删除
    if file_path.suffix in EXCEL_TYPE:
        files = excel_to_csv(file_path.parent, file_path)  # 将excel转换成csv
        keep_file = False
    else:
        files = [file_path]
    result_file = []
    for file in files:
        fpath, fname = file.parent, file.stem
        title = common.read_title(file, skip_row)  # 读取title
        common.print_list_formating(title)  # 打印title
        split_key = input_data('str', '请依次输入[分组索引],[网元名称索引],[脚本索引]')  # 输入分割参数
        split_columns = __get_split_columns(split_key, title)  # 通过正则将分割参数转为list
        # groupby_column:需要分组的列，sitename_column：基站名称列，用于计算基站数量，mml_column：mml脚本列，用于输出mml脚本
        groupby_column, sitename_column, mml_column = split_columns
        print(f'>>>开始分割文件"{file}"')
        tb = pd.read_csv(file, encoding=file_encoding(file), skiprows=skip_row, error_bad_lines=False,
                         low_memory=False)
        grouper = tb.groupby(by=groupby_column, as_index=False, sort=False)  # 按照分组列分组
        print(f'>>>文件"{file}"按照"{"_".join(groupby_column)}"共可分割成{len(grouper)}组')
        for key, value in grouper:
            fid = 0
            save_name_tail = key if isinstance(key, str) else '_'.join(key)
            save_name_tail = replace_invalid_char(save_name_tail)
            sitename = value[sitename_column].drop_duplicates()  # 分组后读取基站名称，并去重
            sitename.reset_index(inplace=True, drop=True)  # 重设index，目的是后边按index分组cut
            bins = [x * site_num for x in range(ceil(len(sitename) / site_num) + 1)]  # 设置cut区间
            if len(bins) > 2:
                sitename['cut'] = pd.cut(sitename.index, bins, right=False)  # 填充cut区间列
                cut_value = sitename.groupby('cut', sort=False, as_index=False)  # 按照cut分组，取其中的sitename，series类型
                for k, names in cut_value:
                    fid += 1
                    save_path = fpath / f'{fname}_{save_name_tail}_{fid}.txt'
                    print(f'>>>生成文件:{save_path}...')
                    result_file.append(save_path)
                    names = names[sitename_column[0]]
                    _tb = value.loc[value[sitename_column[0]].isin(names)]  # 按照cut后sitename，在value中提取数据
                    for mml in mml_column:
                        c = _tb[mml].replace(r'^\s*$', value=np.nan, regex=True).dropna()  # 去除空白元素
                        c.to_csv(save_path, index=False, encoding='gbk', mode='a', header=False, sep='\n',
                                 quoting=csv.QUOTE_NONE)  # quoting=csv.QUOTE_NONE，不添加引号，sep='\n',换行符作为分隔符
            else:
                fid += 1
                save_path = fpath / f'{fname}_{save_name_tail}_{fid}.txt'
                print(f'>>>生成文件:{save_path}...')
                result_file.append(save_path)
                for mml in mml_column:
                    c = value[mml].replace(r'^\s*$', value=np.nan, regex=True).dropna()
                    c.to_csv(save_path, index=False, encoding='gbk', mode='a', header=False, sep='\n',
                             quoting=csv.QUOTE_NONE)  # quoting=csv.QUOTE_NONE，不添加引号，sep='\n',换行符作为分隔符
    for f in result_file:
        if f.stat().st_size > file_size:
            split_by_size(f.parent, f, file_size, keep_file=False)  # 将文件大小超过file_size的文件进行再次分割
    if not keep_file: [f.unlink() for f in files]


def __get_split_columns(split_key, title):
    para_list = []  # 记录将输入字符串转化成list，例如[[1,2],[3,4],[5,6]]
    sp = re.findall(r'\[(.+?)\]', split_key)  # 按照[]拆分成list
    for i in range(len(sp)):
        if '-' not in sp[i]:
            para_list.append(eval('[' + sp[i] + ']'))
        else:
            sp1 = sp[i].split(',')
            lst = []
            for _sp in sp1:
                if _sp.isdigit():
                    lst.append(int(_sp))
                elif '-' in _sp:
                    start, end = _sp.split('-')
                    lst += [x for x in range(int(start), int(end) + 1)]
            lst = list(set(lst))
            para_list.append(lst)

    result_column = []
    for p in para_list:
        result_column.append([title[i - 1] for i in p])
    return result_column
