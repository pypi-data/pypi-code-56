# -*- coding: utf-8 -*-
# @Filename : filesys.py
# @Date : 2018-10-26
# @Update: 2020-05-28
# @Author : liwei

import os


def parse_file(file):
    """Split file path, name and extension

    Args:
        file (str): Input file

    Returns:
        [str]: File path
        [str]: File name
        [str]: File extension
    """
    file_path, file_name_tmp = os.path.split(file)
    file_name, file_ext = os.path.splitext(file_name_tmp)
    return file_path, file_name, file_ext


def create_dirs(dirs):
    """
    Create a list of directories if they don't exist
    Args:
        dirs: a list of directories

    Returns:
        exit_code: True:success False:failed

    """
    try:
        if isinstance(dirs, str):
            if not os.path.exists(dirs):
                os.makedirs(dirs)
        elif isinstance(dirs, list):
            for dir_ in dirs:
                if not os.path.exists(dir_):
                    os.makedirs(dir_)
        return True
    except Exception as err:
        print("Creating directories error: {0}".format(err))
        return False


def files_in_folder(path):
    """Get all the files in a folder

    Args:
        path (str): Input directory

    Returns:
        [list]: file list
    """
    files = os.listdir(path)
    file_list = []
    for file in files:
        if not os.path.isdir(os.path.join(path, file)):
            file_list.append(file)
            # print('++', file)
    return file_list


def folders_in_folder(path):
    folders = os.listdir(path)  # get all the name
    folder_list = []
    for folder in folders:
        # is a file or folder, only process folders
        if os.path.isdir(os.path.join(path, folder)):
            folder_list.append(folder)
            # print('--', folder)
    return folder_list


def rename_file(src_file, new_file):
    os.rename(src_file, new_file)


if __name__ == '__main__':
    pass
