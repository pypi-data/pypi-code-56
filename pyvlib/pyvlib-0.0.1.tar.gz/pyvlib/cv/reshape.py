# -*- coding: utf-8 -*-
# @Filename: reshape.py
# @Date: 2018-10-25
# @Update: 2020-05-28
# @Author: liwei

import os
import numpy as np
import cv2


def resize(image, size):
    resized = cv2.resize(image, size)
    return resized


def rotate(image, angle, center=None, scale=1.0):
    h, w = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    mat = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, mat, (w, h))
    return rotated


def padding(image, size=None):
    """
    padding a rectangular image to a square one with the border pixel of the longer edge
    Args:
        image:
        size: resize the output image

    Returns:

    """
    h, w = image.shape[0], image.shape[1]
    sz = w if w > h else h  # final image size
    dim = image.ndim
    if dim == 2:
        blank_image = np.zeros((sz, sz), np.uint8)
    else:
        _, _, channel = image.shape
        blank_image = np.zeros((sz, sz, channel), np.uint8)

    pad_color = True
    if w > h:
        x0 = 0
        y0 = int((w - h) / 2)
        blank_image[y0:y0 + h, x0:x0 + w] = image
        if pad_color:
            for y in range(0, y0, 1):  # up
                blank_image[y, :] = blank_image[y0, :]
            for y in range(y0 + h, sz, 1):
                blank_image[y, :] = blank_image[y0 + h - 1, :]
    else:
        x0 = int((h - w) / 2)
        y0 = 0
        blank_image[y0:y0 + h, x0:x0 + w] = image
        if pad_color:
            for x in range(0, x0, 1):  # up
                blank_image[:, x] = blank_image[:, x0]
            for x in range(x0 + w, sz, 1):
                blank_image[:, x] = blank_image[:, x0 + w - 1]

    if size is not None:
        blank_image = cv2.resize(blank_image, size)
    return blank_image


if __name__ == "__main__":
    pass
