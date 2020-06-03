# -*- coding: utf-8 -*-
"""
DG dataformat
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import os
import numpy as np


__all__ = ['Input', 'get_pred_boxes', 'make_imglist_roidb', 'get_roidb_batch']


class Input(object):
    """
    input info
    """
    def __init__(self, inputfile, field, task, imgdir, imgrec, videofile):
        self.inputfile = inputfile
        self.field = field
        self.task = task
        self.imgdir = imgdir
        self.imgrec = imgrec
        self.videofile = videofile
        assert inputfile is not None
        assert imgdir is not None or imgrec is not None

    def get_pred_boxes(self, pred_boxes_path):
        all_images = []
        all_pred_boxes = []
        with open(pred_boxes_path) as fn:
            for line in fn.readlines():
                line = [i.strip() for i in line.strip().split(' ')]
                all_images.append(line[0])
                assert len(line) >= 1
                if len(line) == 1:
                    pred_boxes = np.zeros((0, 5), dtype=np.float32)
                else:
                    assert (len(line) - 1) % 5 == 0
                    pred_boxes = np.array(line)[1:].astype(np.float32).reshape((-1, 5))
                all_pred_boxes.append(pred_boxes)
        return all_images, all_pred_boxes

    def make_imglist_roidb(self, imgdir, inputfile, batch_size):
        if inputfile.endswith('.txt') or inputfile.endswith('.lst'):
            all_images, all_pred_boxes = self.get_pred_boxes(inputfile)
            roidb = []
            roi_recs = []
            batch_num = len(all_images) // batch_size
            for i in range(len(all_images)):
                roi_recs.append({'image_path': os.path.join(imgdir, os.path.basename(all_images[i])),
                                 'boxes': all_pred_boxes[i]})
            for i in range(batch_num):
                roidb.append(roi_recs[i * batch_size:(i+1) * batch_size])
            if len(all_images) % batch_size != 0:
                roidb.append(roi_recs[batch_num * batch_size:])
        return roidb

    def get_roidb_batch(self, batch_size):
        return self.make_imglist_roidb(self.imgdir, self.inputfile, batch_size)
