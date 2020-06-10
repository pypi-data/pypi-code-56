from multiprocessing import Pool, cpu_count
from pathlib import Path

from . import EXCEL_TYPE, TXT_TYPE
from .common import get_files
from .parser import transform_file


def excel_to_csv(save_path, workbook_path, **kwargs):
    '''
    将excel转换成csv，每个sheet转换成一个csv文件
    :param save_path: 转换后文件保存路径
    :param workbook_path: excel文件路径
    :param kwargs:
    :return: 转换后的文件列表
    '''
    return transform_file(save_path, workbook_path, engine='excel', **kwargs)


def csv_to_excel(save_path, csv_path, **kwargs):
    '''
    将csv转换成excel格式文件
    :param save_path: 文件保存路径
    :param csv_path: csv文件路径
    :param kwargs:
    :return: 返回转换后的文件路径列表
    '''
    return transform_file(save_path, csv_path, engine='csv', **kwargs)


def excel_to_csv_in_path(save_path, path, all=False, **kwargs):
    '''
    将目录内的额所有excel文件转换为csv文件
    :param save_path: 文件保存路径
    :param path: 目录路径，会在该路径下搜索excel文件
    :param all: 是否递归查找子目录
    :param kwargs:
    :return: 返回转换后的文件路径列表
    '''
    wb_paths = get_files(path, EXCEL_TYPE, all=all)
    process_num = min(cpu_count(), len(wb_paths))
    p = Pool(processes=process_num)
    result = []
    for wb_path in wb_paths:
        res = p.apply_async(excel_to_csv, args=(save_path, wb_path), kwds=kwargs)
        result.append(res)
    p.close()
    p.join()
    return result


def csv_to_excel_in_path(save_path, path, all=False, **kwargs):
    '''
    将目录内的额所有csv文件转换为excel文件
    :param save_path: 文件保存路径
    :param path: 目录路径，会在该路径下搜索csv文件
    :param all: 是否递归查找子目录
    :param kwargs:
    :return: 返回转换后的文件路径列表
    '''
    csv_paths = get_files(path, TXT_TYPE, all=all)
    process_num = min(cpu_count(), len(csv_paths))
    result = []
    p = Pool(process_num)
    for csv_path in csv_paths:
        result.append(p.apply_async(csv_to_excel, args=(save_path, csv_path,), kwds=kwargs))
    p.close()
    p.join()
    return result


def excel_to_csv_in_list(save_path, excel_list, **kwargs):
    '''
    将列表内的excel文件转换成csv文件
    :param save_path: 文件保存路径
    :param excel_list:  excel文件列表
    :param kwargs:
    :return: 返回转换后的文件列表
    '''
    process_num = min(cpu_count(), len(excel_list))
    result = []
    p = Pool(process_num)
    for excel in excel_list:
        if not Path(excel).exists():
            raise ValueError(f'文件{excel}不存在')
        result.append(p.apply_async(excel_to_csv, args=(save_path, excel), kwds=kwargs))
    p.close()
    p.join()
    return result


def csv_to_excel_in_list(save_path, csv_list, **kwargs):
    process_num = min(cpu_count(), len(csv_list))
    result = []
    p = Pool(process_num)
    for csv_file in csv_list:
        if not Path(csv_file).exists():
            raise ValueError(f'文件{csv_file}不存在')
        result.append(p.apply_async(csv_to_excel, args=(save_path, csv_file), kwds=kwargs))
    p.close()
    p.join()
    return result
