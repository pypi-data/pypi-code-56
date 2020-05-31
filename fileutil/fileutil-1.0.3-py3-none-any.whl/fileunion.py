from pathlib import Path

from . import EXCEL_TYPE
from . import common
from .filetransform import excel_to_csv
from .parser import union_file


def union_in_path(save_path, file_path, file_type=EXCEL_TYPE, all=False, engine='normal', skip_row=0,
                  need_title=False, **kwargs):
    save_path, file_path = Path(save_path), Path(file_path)
    if not save_path.exists():
        raise ValueError('保存路径不存在')
    if not file_path.exists():
        raise ValueError('文件搜索路径不存在')
    file_list = common.get_files(file_path, file_type, all)
    need_trans_list_before = list(filter(lambda f: f.suffix in EXCEL_TYPE, file_list))
    no_need_trans_list = [x for x in file_list if x not in need_trans_list_before]
    need_trans_list_after = []
    kwargs.update(skip_row=skip_row, need_title=need_title, file_type=file_type, all=all)
    for file in need_trans_list_before:
        file = Path(file)
        need_trans_list_after += excel_to_csv(file.parent, file, **kwargs)
    need_union_file = need_trans_list_after + no_need_trans_list
    result = union_file(save_path, need_union_file, engine=engine, **kwargs)
    [f.unlink() for f in need_trans_list_after]  # 删除转换时的临时文件
    return result


def union_in_list(save_path, file_list, engine='normal', skip_row=0, need_title=False, **kwargs):
    save_path = Path(save_path)
    if not save_path.exists():
        raise ValueError('保存路径不存在')
    need_trans_list_before = list(filter(lambda f: f.suffix in EXCEL_TYPE, file_list))
    no_need_trans_list = [x for x in file_list if x not in need_trans_list_before]
    need_trans_list_after = []
    kwargs.update(skip_row=skip_row, need_title=need_title)
    for file in need_trans_list_before:
        file = Path(file)
        need_trans_list_after += excel_to_csv(file.parent, file, **kwargs)
    need_union_file = need_trans_list_after + no_need_trans_list
    result = union_file(save_path, need_union_file, engine=engine, **kwargs)
    [f.unlink() for f in need_trans_list_after]  # 删除转换时的临时文件
    return result


def excel_union(save_path, file_path, engine='normal', skip_row=0, need_title=False, **kwargs):
    file_path = Path(file_path)
    kwargs.update(skip_row=skip_row, need_title=need_title)
    csv_list = excel_to_csv(save_path, file_path, **kwargs)
    result = union_in_list(file_path.parent, csv_list, engine=engine, **kwargs)
    [f.unlink() for f in csv_list]
    return result
