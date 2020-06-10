import csv
import time
from csv import writer
from math import ceil
from pathlib import Path

import pandas as pd
import xlsxwriter

from . import TXT_TYPE, EXCEL_TYPE
from .common import replace_invalid_char, read_excel, file_encoding, read_title


def _make_union_function(name):
    def parser_f(save_path, files, engine='normal', skip_row=0, need_title=True, all=False, keep_file=True, **kwargs):
        kwargs.update(
            skip_row=skip_row,
            need_title=need_title,
            all=all,
            keep_file=keep_file,
        )
        return _union_file(save_path, files, engine, **kwargs)

    parser_f.__name__ = name
    return parser_f


def _union_file(save_path, files, engine, **kwargs):
    save_path = Path(save_path)
    if not save_path.exists():
        raise ValueError("文件保存的路径不存在")
    if not files:
        raise ValueError("没有可合并的文件")
    if len(files) == 1:
        raise ValueError('只有一个文件，不需要进行合并')
    not_txt_file = list(filter(lambda x: Path(x).suffix not in TXT_TYPE, files))
    if len(not_txt_file) > 0:
        raise ValueError(f'共{len(not_txt_file)}个文件不属于文本类型，需先对其进行转换\n{not_txt_file}')
    union_dict = {'normal': _normal_union_engine, 'pandas': _pandas_union_engine}
    if engine not in union_dict.keys():
        raise ValueError('输入的文件合并引擎名称不正确')
    union_engine = _pandas_union_engine if engine == 'pandas' else _normal_union_engine
    result = union_engine(save_path, files, **kwargs)
    keep_file = kwargs.get('keep_file', True)
    if not keep_file:
        [f.unlink() for f in files]
    return result


def _normal_union_engine(save_path, files, **kwargs):
    save_path = save_path / f'UnionResult{time.strftime("%Y%m%d%H%M%S", time.localtime())}.csv'
    title = None
    have_title = False
    chunksize = 10 * 1024 * 1024  # 每次读取10m
    need_title = kwargs.get('need_title', False)
    skip_row = kwargs.get('skip_row', 0)
    print('{:-^70}'.format(f'正在合并文件，共需合并{len(files)}个文件'))
    with open(save_path, 'wb') as fobj:
        if len(files) > 1:
            for index, file in enumerate(files):
                with open(file, 'rb') as subobj:
                    for i in range(skip_row):
                        subobj.readline()
                    if need_title:
                        title = subobj.readline()
                    if not have_title and need_title:
                        fobj.write(title)
                        have_title = True
                    while True:
                        chunk = subobj.read(chunksize)
                        if not chunk:
                            break
                        else:
                            fobj.write(chunk)
                print(f'>>>已合并第{index + 1}/{len(files)}个文件:{file}...')
    return save_path


def _pandas_union_engine(save_path, files, **kwargs):
    save_path = save_path / f'UnionResult_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.csv'
    skip_row = kwargs.get('skip_row', 0)
    print('{:-^70}'.format(f'正在合并文件，共需合并{len(files)}个文件'))
    title = []
    for file in files:
        _title = read_title(file, skip_row)
        title += [t for t in _title if t not in title]
    base = pd.DataFrame(columns=title)
    for index, file in enumerate(files):
        tbs = pd.read_csv(file, encoding=file_encoding(file), skiprows=skip_row, chunksize=10000,
                          keep_default_na=False, error_bad_lines=False, low_memory=False)
        for tb in tbs:
            _tb = pd.concat([base, tb])
            _tb.to_csv(save_path, index=False, encoding='gbk', header=not save_path.exists(), mode='a')
        print(f'>>>已合并第{index + 1}/{len(files)}个文件:{file}...')
    return save_path


def _make_split_function(name):
    def parser_f(save_path, files, engine='row', skip_row=0, need_title=True, all=False, keep_file=True,
                 row_num=None, size=None, column=None, **kwargs):
        kwargs.update(
            skip_row=skip_row,
            need_title=need_title,
            all=all,
            keep_file=keep_file,
            row_num=row_num,
            size=size,
            column=column
        )
        return _split_file(save_path, files, engine, **kwargs)

    parser_f.__name__ = name
    return parser_f


def _split_file(save_path, file, engine, **kwargs):
    save_path, file = Path(save_path), Path(file)
    if not save_path.exists():
        raise ValueError("文件保存的路径不正确")
    if not file.exists():
        raise ValueError("没有可分割的文件")

    if file.suffix not in TXT_TYPE:
        raise ValueError('分割文件非文本类型，请先进行转换')

    split_engine_dict = {'row': (_split_by_row_engine, kwargs.pop('row_num', None)),
                         'size': (_split_by_size_engine, kwargs.pop('size', None)),
                         'column': (_split_by_column_engine, kwargs.pop('column', None))}
    if engine not in split_engine_dict.keys():
        raise ValueError('输入的数据分割引擎名称不正确')
    need_title = kwargs.get('need_title', False)
    keep_file = kwargs.get('keep_file', False)
    if need_title is False and engine == 'column':
        raise ValueError('按列分割时需要将need_title设置成True')
    split_engine, para = split_engine_dict[engine][0], split_engine_dict[engine][1]
    if not para:
        print(f'分割引擎设置为{engine}时，必须设置{split_engine_dict[engine][1]}参数')
    result = split_engine(save_path, file, para, **kwargs)
    if not keep_file: file.unlink()
    return result


def _split_by_row_engine(save_path, file, row_num, **kwargs):
    file = Path(file)
    stem, suffix = file.stem, file.suffix
    skip_row = kwargs.get('skip_row', 0)
    need_title = kwargs.get('need_title', False)
    print('{:-^70}'.format(f'正在分割文件:{file.name}'))
    fid = 0
    mew_file_list = []
    with open(file, mode='rb') as fobj:
        for i in range(skip_row):
            fobj.readline()
        if need_title: title = fobj.readline()
        while True:
            line = fobj.readline()
            if not line: break
            fid += 1
            _save_path = Path(save_path) / f'{stem}_{fid}{suffix}'
            sub_obj = open(_save_path, mode='wb')
            if need_title: sub_obj.write(title)
            sub_obj.write(line)
            for i in range(row_num - 1):
                line = fobj.readline()
                if not line:
                    break
                sub_obj.write(line)
            sub_obj.close()
            mew_file_list.append(_save_path)
            print(f'>>>生成文件:{_save_path}')
    return mew_file_list


def _split_by_size_engine(save_path, file, split_size, **kwargs):
    stem, suffix = file.stem, file.suffix
    need_title = kwargs.get('need_title', False)
    skip_row = kwargs.get('skip_row', False)
    chunksize = 10 * 1024 * 1024  # 每次读取10mb
    fsize = file.stat().st_size  # 文件总大小
    split_size = int(split_size)
    currentsize = 0  # 当前已读取的大小
    new_file_list = []
    print('{:-^70}'.format(f'文件转换:将{file}转换为csv格式'))
    with open(file, mode='rb') as fobj:
        if skip_row:
            for i in range(0, skip_row):
                currentsize += len(fobj.readline())
        if need_title:
            title = fobj.readline()
            currentsize += len(title)
        fsize -= currentsize
        chunknum = int(split_size // chunksize)  # 计算每个文件需要chunk次数
        split_num = ceil(fsize / split_size)  # 计算可分割多少个文件
        print(f'>>>正在分割文件"{stem}{suffix}",总大小{round(fsize / 1024 / 1024, 2)}mb,共需分割{split_num}次')
        for i in range(split_num):
            _save_path = save_path / f'{stem}_{i + 1}{suffix}'
            with open(_save_path, mode='wb') as subobj:
                if title: subobj.write(title)
                havechunk = 0
                for j in range(chunknum):
                    subobj.write(fobj.read(chunksize))
                    havechunk += chunksize
                subobj.write(fobj.read(split_size - havechunk))  # 如果剩余大小不足chunk一次，写入余量

                subobj.write(fobj.readline())
            new_file_list.append(_save_path)
            print(
                f'>>>文件"{stem}"第{i + 1}/{split_num}次分割，生成文件:{_save_path}')
    return new_file_list


def _split_by_column_engine(save_path, file, split_column, **kwargs):
    stem, suffix = file.stem, file.suffix
    skip_row = kwargs.get('skip_row', 0)
    if isinstance(skip_row, list) and isinstance(skip_row, str):
        raise ValueError('需分割的列的参数格式不正确')
    encode = file_encoding(file)
    tbs = pd.read_csv(file, encoding=encode, skiprows=skip_row, header=0, chunksize=100000,
                      keep_default_na=False, low_memory=False, error_bad_lines=False)
    print('{:-^70}'.format(f'文件分割:将{file}按照{",".join(split_column)}'))
    new_file_list = []
    for tb in tbs:
        group = tb.groupby(split_column)
        for index, value in group:
            savename_tail = str(index) if len(split_column) == 1 else '_'.join(
                [str(x) for x in index])
            savename_tail = replace_invalid_char(savename_tail)
            _save_path = save_path / f'{stem}_{savename_tail}{suffix}'

            header = not _save_path.exists()
            if header: print(f'>>>生成文件：{_save_path}')
            value.to_csv(_save_path, index=False, encoding='gbk', mode='a', header=header)
            new_file_list.append(_save_path)
    return list(set(new_file_list))


def _excel_trans_engine(save_path, workbook_path, **kwargs):
    workbook_path = Path(workbook_path)
    name, stem = workbook_path.name, workbook_path.stem
    print('{:-^70}'.format(f'文件转换:将{workbook_path.name}转换为csv格式'))
    file_list = []
    for sheet in read_excel(workbook_path):
        if sheet.visibility == 0:
            if sheet.nrows > 0 and sheet.ncols > 0:
                sheet_name = replace_invalid_char(sheet.name)
                _save_path = Path(save_path) / f'{stem}_{sheet_name}.csv'
                file_list.append(_save_path)
                print(f'转换文件：{_save_path}')
                with open(_save_path, 'w', encoding='gbk', newline='') as f:
                    w = writer(f, dialect='excel')
                    for i in range(sheet.nrows):
                        w.writerow(sheet.row_values(i))
    return file_list


def _csv_trans_engine(save_path, csv_path, **kwargs):
    csv_path = Path(csv_path)
    fpath, fstem, fname = csv_path.parent, csv_path.stem, csv_path.name
    encode = file_encoding(csv_path)
    print('{:-^70}'.format(f'文件转换:将{fname}转换为excel格式'))
    file_list = []
    fobj = open(csv_path, 'r', encoding=encode, )
    save_path = Path(save_path) / f'{fstem}.xlsx'
    wb = xlsxwriter.Workbook(save_path)
    ws = wb.add_worksheet(fstem)
    lines = csv.reader(fobj)
    for index, line in enumerate(lines):
        ws.write_row(index, 0, line)
    wb.close()
    fobj.close()
    file_list.append(save_path)
    print(f'生成文件：{save_path}.$Sheet["{ws.name}"]')
    return file_list


def _make_trans_function(name):
    def parser_f(save_path, file_path, engine='excel', keep_file=True, **kwargs):
        kwargs.update(
            keep_file=keep_file
        )
        return _transform_file(save_path, file_path, engine, **kwargs)

    parser_f.__name__ = name
    return parser_f


def _transform_file(save_path, file_path, engine, **kwargs):
    save_path = Path(save_path)
    if not save_path.exists():
        raise ValueError("文件保存的路径不正确")
    if not file_path:
        raise ValueError("没有可转换的文件")
    file = Path(file_path)
    transform_dict = {'csv': _csv_trans_engine,
                      'excel': _excel_trans_engine
                      }
    if not save_path.exists():
        raise ValueError('存储路径不存在')
    if not file_path:
        raise ValueError('需转换的文件不存在')
    if engine not in transform_dict.keys():
        raise ValueError('输入的文件转换引擎名称不正确')
    if (file.suffix in EXCEL_TYPE and engine != 'excel') or (file.suffix in TXT_TYPE and engine != 'csv'):
        raise ValueError('文件类型与转换引擎不符合')
    trans_engine = _csv_trans_engine if engine == 'csv' else _excel_trans_engine
    result = trans_engine(save_path, file_path, **kwargs)
    keep_file = kwargs.get('keep_file', True)
    if not keep_file:
        [f.unlink() for f in file_path]
    return result


union_file = _make_union_function('union_file')
split_file = _make_split_function('split_file')
transform_file = _make_trans_function('transform_file')
