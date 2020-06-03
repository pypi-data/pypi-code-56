# -*- coding: utf-8 -*-
# @Filename: mask.py
# @Date: 2018-10-25
# @Update: 2020-05-28
# @Author: liwei

import os
import numpy as np
import cv2

__all__ = ['get_mask', 'extract']


def get_mask(image, threshold=1):
    if image.ndim == 3:
        mask = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif image.ndim == 3:
        mask = image.copy()
    else:
        raise ValueError('wrong image dim')
    mask[mask >= threshold] = 255
    return mask


def extract(image, mask, threshold=1, kernel_size=0):
    """Extract the mask region, set the pixels outside the mask to zero

    Args:
        image (): Input image
        mask ([type]): Input gray image
        threshold (int, optional): Threshold to generate binary mask. Defaults to 1.
        kernel_size (int, optional): Kernel size to erode(<0) or dilate(>0) mask. Defaults to 0.

    Returns:
        [type]: Output image
    """
    if kernel_size < 0:
        sz = -kernel_size
        kernel = np.ones((sz, sz), np.uint8)
        mask_bin = cv2.erode(((mask > threshold)).astype(
            np.uint8), kernel, iterations=1)
    elif kernel_size > 0:
        sz = kernel_size
        kernel = np.ones((sz, sz), np.uint8)
        mask_bin = cv2.dilate(((mask > threshold)).astype(
            np.uint8), kernel, iterations=1)
    else:
        mask_bin = np.where((mask > threshold), 1, 0).astype('uint8')

    img_fg = image * mask_bin[:, :, np.newaxis]
    return img_fg


if __name__ == '__main__':
    pass
