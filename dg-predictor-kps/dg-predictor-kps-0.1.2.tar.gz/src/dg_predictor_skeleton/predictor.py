# -*- coding: utf-8 -*-
""" multitask predictor
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import mxnet as mx
import numpy as np
import cv2
import copy
import logging
from collections import namedtuple, OrderedDict

from dg_predictor import BasePredictor
from dg_predictor.utils import (
    resize_image, generate_new_boxes, crop_and_resize_image)
from .dg_ltpl_skeleton import Decoder


__all__ = ['create']


def create(config):
    """
    factory method
    """
    return Predictor(config)


TASKS = ['unknown', 'det', 'kps', 'kps_heatmap', 'kps_offset', 'reid', 'mask']


class Predictor(BasePredictor):
    def __init__(self, config):
        super(Predictor, self).__init__(config, task_name='skeleton')
        self.config = config
        self.create_source()
        self.create_predictor()
        self.get_input_shape()
        self.decoder = Decoder(self.config.num_kps, 25.6, 25.6, 16)
        self.input_mean = np.array(self.config.input_mean, dtype=np.float32).reshape((1, 3, 1, 1))
        self.input_scale = np.array(self.config.input_scale, dtype=np.float32).reshape((1,))
        self.config.save = getattr(self.config, 'save', '%s_outputs.txt' % self.task_name)

        assert hasattr(self.config, 'task')
        for each_task in self.config.task:
            assert each_task[0] in TASKS, "not support task %s" % each_task
            if each_task[0] == 'det':
                self.det_cnt += 1
        # save task name to list
        self.task_types = list()
        for each_task in self.config.task:
            self.task_types.append(each_task[0])

        self.save_file = open(self.config.save, 'w')

    def get_input_shape(self):
        self.input_shape = [int(i) for i in self.config.input_shape.split(',')]
        self.input_height = self.input_shape[0]
        self.input_width = self.input_shape[1]

    def pre_process(self):
        """
        info_batch => data_batch
        """
        data_list = list()
        for k, this_info in enumerate(self.info_batch):
            try:
                img = cv2.imread(this_info['image_path'], cv2.IMREAD_COLOR)
                self.info_batch[k]['image_ok'] = True
            except Exception as e:
                logging.info("loading image %s error" % this_info['image_path'])
                img = np.zeros(self.input_shape, dtype=np.uint8)
                self.info_batch[k]['image_ok'] = False
            if img is None:
                img = np.zeros(self.input_shape, dtype=np.uint8)
                self.info_batch[k]['image_ok'] = False

            if self.info_batch[k]['image_ok']:
                img_h, img_w, _ = img.shape
                # change image format
                if self.config.input_format == 'gray':
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = np.reshape(img, (img.shape[0], img.shape[1], 1))
                elif self.config.input_format == 'rgb':
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                elif self.config.input_format == 'bgr':
                    img = img
                else:
                    assert False, 'not support input format (gray, rgb, bgr, yuv444)'
                # padding to input_shape

                boxes = this_info['boxes']
                if len(boxes) > 0:
                    img, _ = resize_image(img, 1.0, 32)
                    aspect_ratio = float(self.config.pooled_size[0] / self.config.pooled_size[1])
                    boxes, _ = generate_new_boxes(
                                    boxes=boxes,
                                    new_num_boxes=len(boxes),
                                    rescale_factor=0.1,
                                    aspect_ratio=aspect_ratio)
                    boxes = boxes.astype(np.int32)
                    imgs = crop_and_resize_image(img, boxes,
                                                 dst_shape=tuple(self.input_shape[:2][::-1]))
                    for img in imgs:
                        data_list.append(img[np.newaxis, :])

                    self.info_batch[k]['_boxes'] = boxes.astype(np.float32)
                    self.info_batch[k]['_classes'] = np.ones((len(boxes),),
                                                 dtype=np.int32)
                else:
                    self.info_batch[k]['_boxes'] = np.zeros((0, 4), dtype=np.float32)
                    self.info_batch[k]['_classes'] = np.zeros((0,), dtype=np.int32)

        if len(data_list) > 0:
            data = np.vstack(data_list)
            data = data.transpose((0, 3, 1, 2))
            data = (data - self.input_mean) * self.input_scale

        self.data_batch = mx.nd.array(data, dtype=data.dtype)

    def post_process(self):
        data = [output.asnumpy() for output in self.network_outputs]
        assert 'kps' in self.config.task[0], "This a kps task!"
        num_kps = self.config.num_kps
        kps_output = data[0]
        num_images = len(self.info_batch)
        cur_num = 0
        for n in range(num_images):
            num_boxes = len(self.info_batch[n]['_boxes'])
            kps_output_n = kps_output[cur_num: cur_num+num_boxes]
            cur_num += num_boxes
            kps_scores_n = kps_output_n[:, :num_kps, :, :]
            kps_deltas_n = kps_output_n[:, num_kps:, :]
            self.info_batch[n]['kps_pred'] = self.decoder(kps_scores_n, kps_deltas_n, self.info_batch[n])

    def save_result(self):
        # save to file
        file_fid = self.save_file
        for this_info in self.info_batch:
            if not this_info['image_ok']:
                continue
            boxes = this_info['_boxes']
            save_string = ''
            save_string += this_info['image_path']
            for ind, bbox in enumerate(boxes):
                if 'kps_pred' in this_info:
                    save_string += ' '
                    save_string += (' '.join('%.4f' % x for x in this_info['kps_pred'][ind]))
            save_string += '\n'
            file_fid.write(save_string)


    def __del__(self):
        if hasattr(self, 'save_file'):
            self.save_file.close()
