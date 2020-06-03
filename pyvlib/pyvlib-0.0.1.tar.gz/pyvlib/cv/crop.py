# -*- coding: utf-8 -*-
# @Filename: crop.py
# @Date: 2019-5-26
# @Update: 2020-05-28
# @Author: liwei


import os
import numpy as np
import cv2


def crop(image, border=10):
    """
    crop image with black background by a rectangle
    Args:
        image: input image of size [w,h] or [w,h,c]
        border: border width when cropping
    Returns:
        cropped image
    Ref:
        https://codereview.stackexchange.com/questions/132914/crop-black-border-of-image-using-numpy
    """

    dim = image.ndim
    assert (dim == 2 or dim == 3)

    if dim == 2:
        w, h = image.shape
        # Mask of non-black pixels (assuming image has a single channel).
        mask = image > 0
    else:
        w, h, channel = image.shape
        if channel == 4:  # [w,h,4]
            mask = image[:, :, 3] > 0
        else:  # [w,h,3] or [w,h,1]
            mask = image[:, :, 0] > 0
    coords = np.argwhere(mask[:, :])  # Coordinates of non-black pixels.

    # Bounding box of non-black pixels.
    x0, y0 = coords.min(axis=0)
    x1, y1 = coords.max(axis=0) + 1  # slices are exclusive at the top

    cropped_w = x1 - x0
    cropped_h = y1 - y0
    if dim == 2:  # [w,h]
        cropped = np.zeros(
            (cropped_w + 2 * border, cropped_h + 2 * border), np.uint8)
    else:         # [w,h,c]
        _, _, channel = image.shape
        cropped = np.zeros(
            (cropped_w + 2 * border, cropped_h + 2 * border, channel), np.uint8)
    cropped[border:cropped_w+border,
            border:cropped_h+border] = image[x0:x1, y0:y1]

    # x0 = 0 if x0 - border < 0 else x0 - border
    # y0 = 0 if y0 - border < 0 else y0 - border
    # x1 = w - 1 if x1 + border > w - 1 else x1 + border
    # y1 = h - 1 if y1 + border > h - 1 else y1 + border

    # # Get the contents of the bounding box.
    # cropped = image[x0:x1, y0:y1]
    return cropped


def crop_square(image, border=10, size=None):
    """
    crop image with a square

    Args:
        image: Input image
        border: Border size
        size: Final image size, like (512,512)

    Returns:
        Output image

    """
    rect_crop = crop(image, border=border)
    h, w = rect_crop.shape[0], rect_crop.shape[1]
    sz = w if w > h else h   # final image size
    dim = image.ndim
    if dim == 2:  # [w,h]
        blank_image = np.zeros((sz, sz), np.uint8)
    else:         # [w,h,c]
        _, _, channel = image.shape
        blank_image = np.zeros((sz, sz, channel), np.uint8)
    if w > h:
        x0 = 0
        y0 = int((w-h)/2)
        blank_image[y0:y0+h, x0:x0+w] = rect_crop
    else:
        x0 = int((h-w)/2)
        y0 = 0
        blank_image[y0:y0 + h, x0:x0 + w] = rect_crop

    if size is not None:
        blank_image = cv2.resize(blank_image, size)
    return blank_image


def test_crop_image():
    file = './data/girl.png'
    img = cv2.imread(file)
    img_crop = crop_square(img, 30, (512, 512))
    cv2.imshow('img_crop', img_crop)
    cv2.waitKey()


if __name__ == "__main__":
    test_crop_image()
