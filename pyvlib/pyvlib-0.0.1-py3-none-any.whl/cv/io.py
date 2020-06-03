# -*- coding: utf-8 -*-
# @Filename: io.py
# @Date: 2018-10-25
# @Update: 2020-05-28
# @Author: liwei

import os
import numpy as np
import cv2


def read_image(file, fmt='rgb', type=np.uint8, viz=False):
    """[summary]

    Args:
        file (str): Input image file
        fmt (str): Image format, rgb, rgb, gray, grey, rgba, bgra
        type (type, optional): np.uint8, np.float32, np.float64. Defaults to np.uint8.
        viz (bool): If True, show the image

    Returns:
        [type]: Image
    """

    if fmt == 'bgr':
        img = cv2.imread(file, cv2.IMREAD_COLOR)
    elif fmt == 'rgb':
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif fmt == 'gray' or fmt == 'grey':
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    elif fmt == 'rgba':
        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    elif fmt == 'bgra':
        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    else:
        raise ValueError('Wrong image format')

    if viz:
        _, file_name = os.path.split(file)
        cv2.imshow(file_name, img)
        cv2.waitKey(0)

    img = img.astype(type)

    return img


def read_image_sequence(path, ext='png'):
    images = []
    for file_name in os.listdir(path):
        if file_name.endswith(ext):
            file_path = os.path.join(path, file_name)
            images.append(cv2.imread(file_path))
    return images


def save_image(file, img):
    cv2.imwrite(file, img)


if __name__ == "__main__":
    pass
