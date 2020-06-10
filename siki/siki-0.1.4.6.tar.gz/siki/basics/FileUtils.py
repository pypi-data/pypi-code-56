# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Create: May 31, 2018
# Modified: May 25, 2020

import ntpath
import re

from siki.basics import Convert
from siki.basics.Exceptions import NoAvailableResourcesFoundException
from siki.basics.Exceptions import InvalidParamException

def gen_folder_path(prev: str, *last: list):
    import os

    directory = prev
    for strL in last:
        directory = os.path.join(directory, strL)
    return directory


def gen_file_path(folder: str, filename: str, suffix: str = None, addition: str = None):
    import os
    directory = os.path.join(folder, gen_filename(filename, suffix, addition))
    return os.path.abspath(directory)


def gen_filename(filename: str, suffix: str = None, addition: str = None):
    if suffix is None and addition is not None:
        return filename + "." + addition
    if suffix is None and addition is None:
        return filename
    if suffix is not None and addition is None:
        return filename + "." + suffix

    return filename + "." + addition + "." + suffix


def read_file(file_path: str, read_size: int = 4096, callback: object = None):
    with open(file=file_path, mode="rb") as f:

        if not f.readable():
            raise NoAvailableResourcesFoundException("Cannot load file itself")

        if callback is not None:
            data = f.read(read_size)
            while data is not None and len(data) > 0:
                callback(data)
                data = f.read(read_size)
        else:
            return f.read()


def read_file_by_line(file_path: str, callback: object = None):
    # read whole file content
    data = read_file(file_path)

    if data is not None and len(data) > 0:
        str_context = Convert.binary_to_string(data)
        lines = str_context.split('\n')

        for line in lines:
            yield line

    else:
        yield ''


def write_file(file_path: str, data: object, append=False):
    # data is null
    if not data:
        raise NoAvailableResourcesFoundException("Data cannot be null or empty")

    # file path is null
    if not file_path:
        raise NoAvailableResourcesFoundException("File path is incorrect")

    # list conversion
    if isinstance(data, list):
        data = Convert.list_to_string(data)

    # dictionary conversion
    if isinstance(data, dict):
        data = Convert.dict_to_string(data)

    # neither str nor bytes
    # trying to convert the data to string
    if not isinstance(data, str) and not isinstance(data, bytes):
        data = str(data)

    # data is bytes
    if isinstance(data, bytes):
        if append:
            f = open(file=file_path, mode='a+b')
        else:
            f = open(file=file_path, mode='wb')

    # data is str
    elif isinstance(data, str):
        if append:
            f = open(file=file_path, mode='a+')
        else:
            f = open(file=file_path, mode='w')

    else:
        raise InvalidParamException('Cannot write data to file, because of unknown type of data')

    if f is None or not f.writable():
        raise NoAvailableResourcesFoundException("Cannot write file")

    # write file
    f.write(data)
    f.close()


def touch_file(file_path: str):
    """
    Calling this method will create an empty file
    """
    f = open(file_path, "w")
    f.close()


def mkdir(directory: str):
    """
    Calling this method will create an empty folder
    """
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)


def rmfile(file_path: str):
    """
    Calling this method will delete a single file forcely
    """
    import os
    if not os.path.exists(file_path):
        raise NoAvailableResourcesFoundException("File path is not existed!")
    os.remove(file_path)


def rmdir(directory: str):
    """
    Calling this method will delete the folder forcely
    """
    import shutil
    import os
    if not os.path.exists(directory):
        raise NoAvailableResourcesFoundException("Directory path is not existed!")
    shutil.rmtree(directory, ignore_errors=True)


def isfile(path: str):
    import os
    return os.path.isfile(path)


def isdir(path: str):
    import os
    return os.path.isdir(path)


def exists(path: str):
    import os
    return os.path.lexists(path)


def move(path1: str, path2: str):
    from shutil import move
    # no file src exists
    if exists(path1):
        move(path1, path2)


def copy(path1: str, path2: str):  # just trying to copy file
    from shutil import copy2, copytree
    if exists(path1) and isfile(path1):
        copy2(path1, path2)
    if exists(path1) and isdir(path1):
        copytree(path1, path2)


def search_files(folder_path: str, pattern: str = "*"):
    file_list = _file_ite(folder_path)
    return _file_filtering(file_list, pattern)


def search_folders(folder_path: str):
    import os
    dir_list = []
    for i in os.listdir(folder_path):
        path = os.path.join(folder_path, i)
        if os.path.isdir(path):
            dir_list.extend(search_folders(path))
        dir_list.append(path)
    return dir_list


def root_leaf(path: str):
    """
    return root, leaf
    """
    head, tail = ntpath.split(path)
    return ntpath.basename(head), tail


def _file_ite(folder_path: str):
    import os

    file_list = []
    for i in os.listdir(folder_path):
        path = os.path.join(folder_path, i)
        if os.path.isdir(path):
            file_list.extend(_file_ite(path))
        else:
            file_list.append(path)
    return file_list


def _file_filtering(lfs, pattern):
    file_list = []
    if "*" == pattern:
        file_list.extend(lfs)
    else:
        for f in lfs:
            if re.search(pattern, f):
                file_list.append(f)
    return file_list
