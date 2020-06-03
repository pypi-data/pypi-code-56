# -*- coding: utf-8 -*-
# @Filename : fileio.py
# @Date : 2018-10-22
# @Author : liwei

import os
import h5py
import pickle
import numpy as np


def read_dict(file):
    """Read dict file

    Args:
        file (str): Input file, *.pkl, *.npz or *.h5

    Raises:
        ValueError: Wrong file

    Returns:
        dict: dict data
    """
    if file.endsWith(".pkl"):
        return read_pkl(file)
    elif file.endsWith('.npz'):
        return read_npz(file)
    else:
        raise ValueError('Wrong file, support *.pkl, *.npz only')


def read_npy(npy_file):
    npy_data = np.load(npy_file)
    return npy_data


def read_pkl(pkl_file):
    """[summary]

    Args:
        pkl_file ([type]): [description]

    Returns:
        [type]: [description]
    """
    with open(pkl_file, 'rb') as f:
        # pkl_data = pickle.load(f, encoding='iso-8859-1')
        pkl_data = pickle.load(f, encoding='latin1')
        if not isinstance(pkl_data, dict):
            pkl_data = vars(pkl_data)
        if False:
            for key in pkl_data.keys():
                print('key ->', key, 'type=', type(pkl_data[key]))
    return pkl_data


def read_npz(npz_file):
    npz_data = np.load(npz_file)
    if False:
        for key in npz_data.keys():
            print('key ->', key, 'type=', type(npz_data[key]))
    return npz_data


def save_pkl_as_hdf5(pkl_file, hdf_file):
    """

    Args:
        pkl_file: input pkl file, string or dict
        hdf_file: output h5 file, string

    Returns:

    """
    pkl_data = None
    if isinstance(pkl_file, str):
        pkl_data = read_pkl(pkl_file)
    elif isinstance(pkl_file, dict):
        pkl_data = pkl_file
    else:
        assert ValueError('wrong pkl_file')

    hf = h5py.File(hdf_file, mode='w')
    for key in pkl_data.keys():
        print('save', key, 'type=', type(pkl_data[key]))
        if key == 'random_state':
            continue
        data = pkl_data[key]
        if key == 'sequence':
            data = data.tolist()
        if key == 'genders':
            data = [n.encode("ascii", "ignore") for n in data]
        hf.create_dataset(key, data=data)
    hf.close()


def save_dict_as_bin(dict_file, bin_file):
    """Save dict as binary file

    Args:
        dict_file ([type]): input dict file
        bin_file ([type]): output binary file
    """
    dict_data = None
    if isinstance(dict_file, str):
        dict_data = read_dict(dict_file)
    elif isinstance(dict_file, dict):
        dict_data = dict_file
    else:
        assert ValueError('wrong dict_file')

    with open(bin_file, 'wb') as f:
        for key in dict_data.keys():
            # print('save', key, 'type=', type(dict_data[key]))
            data = dict_data[key]
            f.write(key)
            f.write(data)


if __name__ == '__main__':
    pass
