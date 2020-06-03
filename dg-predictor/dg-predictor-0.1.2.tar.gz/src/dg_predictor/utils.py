"""
Utilities
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
import cv2
import math


__all__ = ['limit_roi', 'resize_image', 'generate_new_boxes', 'crop_and_resize_image']


def limit_roi(roi, im_height, im_width):
    """limit roi to image border"""
    left = min(im_width-1, max(0, roi[0]))
    top = min(im_height-1, max(0, roi[1]))
    right = min(im_width-1, max(0, roi[2]))
    bottom = min(im_height-1, max(0, roi[3]))
    return [left, top, right, bottom]


def resize_image(im, size, stride=0, interpolation=cv2.INTER_LINEAR):
    """
    only resize input image to target size and return scale
    :param im: BGR image input by opencv
    :param target_size: one dimensional size (the short side)
    :param max_size: one dimensional max size (the long side)
    :param stride: if given, pad the image to designated stride
    :param interpolation: if given, using given interpolation method to resize image
    :return:
    """
    if isinstance(size, tuple) or isinstance(size, list):
        target_size = size[0]
        max_size = size[1]
        im_shape = im.shape
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])
        im_scale = float(target_size) / float(im_size_min)
        # prevent bigger axis from being more than max_size:
        if np.round(im_scale * im_size_max) > max_size:
            im_scale = float(max_size) / float(im_size_max)
    else:
        im_scale = size
    if im_scale != 1:
        im = cv2.resize(im, None, None, fx=im_scale, fy=im_scale, interpolation=interpolation)

    if stride == 0:
        return im, im_scale
    else:
        # pad to product of stride
        im_height = int(np.ceil(im.shape[0] / float(stride)) * stride)
        im_width = int(np.ceil(im.shape[1] / float(stride)) * stride)
        im_channel = im.shape[2]
        padded_im = np.zeros((im_height, im_width, im_channel), dtype=im.dtype)
        padded_im[:im.shape[0], :im.shape[1], :] = im
        return padded_im, im_scale


def generate_new_boxes(boxes, new_num_boxes, rescale_factor=0.0,
                       jitter_center=False, aspect_ratio=0.0):
    num_boxes = boxes.shape[0]
    assert num_boxes > 0
    if num_boxes == new_num_boxes:
        all_inds = range(num_boxes)
    elif num_boxes > new_num_boxes:
        all_inds = np.random.choice(range(num_boxes), size=new_num_boxes,
                                    replace=False)
    else:
        all_inds = np.array(range(num_boxes))
        while all_inds.shape[0] < new_num_boxes:
            ex_size = np.minimum(num_boxes, new_num_boxes - all_inds.shape[0])
            ex_inds = np.random.choice(range(num_boxes), size=ex_size,
                                       replace=False)
            all_inds = np.append(all_inds, ex_inds)
    assert len(all_inds) == new_num_boxes

    new_boxes = np.zeros((new_num_boxes, 4), dtype=np.float32)
    for i in range(new_num_boxes):
        box = boxes[all_inds[i], :]
        width = box[2] - box[0] + 1
        height = box[3] - box[1] + 1
        if isinstance(rescale_factor, list):
            rand_x1 = random.uniform(rescale_factor[0], rescale_factor[1])
            rand_y1 = random.uniform(rescale_factor[0], rescale_factor[1])
            if jitter_center:
                rand_x2 = random.uniform(rescale_factor[0], rescale_factor[1])
                rand_y2 = random.uniform(rescale_factor[0], rescale_factor[1])
            else:
                rand_x2 = rand_x1
                rand_y2 = rand_y1
        else:
            rand_x1 = rescale_factor
            rand_y1 = rescale_factor
            rand_x2 = rescale_factor
            rand_y2 = rescale_factor
        new_x1 = box[0] - width * rand_x1
        new_y1 = box[1] - height * rand_y1
        new_x2 = box[2] + width * rand_x2
        new_y2 = box[3] + height * rand_y2
        if aspect_ratio > 0:
            new_center_x = (new_x1 + new_x2) / 2
            new_center_y = (new_y1 + new_y2) / 2
            new_width = new_x2 - new_x1 + 1
            new_height = new_y2 - new_y1 + 1
            if aspect_ratio * new_width > new_height:
                new_height = aspect_ratio * new_width
            else:
                new_width = new_height / aspect_ratio
            new_x1 = new_center_x - 0.5 * (new_width - 1)
            new_y1 = new_center_y - 0.5 * (new_height - 1)
            new_x2 = new_center_x + 0.5 * (new_width - 1)
            new_y2 = new_center_y + 0.5 * (new_height - 1)
        if new_x2 < new_x1:
            new_x1, new_x2 = new_x2, new_x1
        if new_y2 < new_y1:
            new_y1, new_y2 = new_y2, new_y1
        new_boxes[i, 0] = new_x1
        new_boxes[i, 1] = new_y1
        new_boxes[i, 2] = new_x2
        new_boxes[i, 3] = new_y2
    return new_boxes, all_inds


def crop_and_resize_image(im, boxes, dst_shape,
                          interpolation=cv2.INTER_LINEAR):
    # im: (h, w, 3)
    # boxes: (num_boxes, 4)
    # dst_shape : (2,) --> dw, dh
    # dst_im: (num_boxes, dh, dw, 3)
    boxes = boxes.astype(np.int32)
    num_boxes = len(boxes)
    dst_im_list = []
    for i in range(num_boxes):
        roi = boxes[i]
        cut_roi = limit_roi(roi, im.shape[0], im.shape[1])
        im_roi = im[cut_roi[1]:cut_roi[3]+1, cut_roi[0]:cut_roi[2]+1, :]
        im_roi = cv2.copyMakeBorder(im_roi,
                                    cut_roi[1] - roi[1],
                                    roi[3] - cut_roi[3],
                                    cut_roi[0] - roi[0],
                                    roi[2] - cut_roi[2],
                                    cv2.BORDER_CONSTANT)
        im_roi = cv2.resize(im_roi, dst_shape, interpolation=interpolation)
        dst_im_list.append(im_roi)
    return dst_im_list
