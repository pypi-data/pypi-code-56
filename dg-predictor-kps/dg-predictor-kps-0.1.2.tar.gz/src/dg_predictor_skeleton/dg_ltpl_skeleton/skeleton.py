# -*- coding: utf-8 -*-
"""label-target-predict convert utility in skeleton task"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
import mxnet as mx


__all__ = ['Decoder']


def smoothen(kps_scores, feat_height, feat_width, gauss_sigma):
    kps_scores = kps_scores.reshape((-1, 1, feat_height, feat_width))

    kps_scores = mx.nd.array(kps_scores)
    
    kernel_x = np.arange(-1, 2)
    kernel_y = np.arange(-1, 2)

    kernel_x, kernel_y = np.meshgrid(kernel_x, kernel_y)

    kernel_x = kernel_x.reshape((-1,))
    kernel_y = kernel_y.reshape((-1,))

    dist = kernel_x ** 2 + kernel_y ** 2

    kernel = np.exp(dist / (-2.0 * gauss_sigma * gauss_sigma))

    kernel = mx.nd.array(kernel.reshape(1, 1, 3, 3))

    kps_scores = mx.nd.Convolution(
                        data=kps_scores,
                        weight=kernel,
                        kernel=(3, 3),
                        num_filter=1,
                        pad=(1, 1),
                        stride=(1, 1),
                        no_bias=True)

    return kps_scores.asnumpy().reshape((-1, feat_height * feat_width))


class Decoder(object):
    """Target to predict transform for skeleton task

    """
    def __init__(self, num_kps, 
                 kps_pos_distance_x, 
                 kps_pos_distance_y, 
                 kps_feat_stride):
        self.num_kps = num_kps
        self.kps_pos_distance_x = kps_pos_distance_x
        self.kps_pos_distance_y = kps_pos_distance_y
        self.kps_feat_stride = kps_feat_stride

        self.do_pixel = True
        self.do_vote = False
        self.do_fix = False
        self.do_approx = False
        assert self.do_vote <= self.do_fix
        assert self.do_approx <= self.do_fix
        assert self.do_fix <= self.do_pixel

    def __call__(self, kps_scores, kps_deltas, roi_list):
        """Convert target to predict
        rois: (num_boxes, 4)
        kps_scores: (num_boxes, num_kps, feat_height, feat_width)
        kps_deltas: (num_boxes, num_kps * 2, feat_height, feat_width)
        """
        num_boxes = kps_scores.shape[0]
        feat_height = kps_scores.shape[2]
        feat_width = kps_scores.shape[3]
        num_kps = self.num_kps

        rois = roi_list['_boxes']
        assert len(rois) == num_boxes

        origin_xy = rois[:, :2]
        origin_xy = np.tile(origin_xy, (1, num_kps))
        origin_xy = origin_xy.reshape((num_boxes * num_kps, 2))

        scales_xy = np.zeros((num_boxes, 2), dtype=np.float32)
        scales_xy[:, 0] = feat_width / (rois[:, 2] - rois[:, 0] + 1)
        scales_xy[:, 1] = feat_height / (rois[:, 3] - rois[:, 1] + 1)
        scales_xy = np.tile(scales_xy, (1, num_kps))
        scales_xy = scales_xy.reshape((num_boxes * num_kps, 2))

        kps_scores = kps_scores.reshape((num_boxes * num_kps, -1))
        kps_deltas = kps_deltas.reshape((num_boxes * num_kps, 2, -1))

        if self.do_pixel:
            kps_scores = smoothen(kps_scores, feat_height, feat_width, gauss_sigma=1.0)

        all_inds = np.arange(num_boxes * num_kps)
        max_inds = kps_scores.argmax(axis=1)
        max_scores = kps_scores[all_inds, max_inds]
        max_inds_xy = np.zeros((num_boxes * num_kps, 2))

        max_inds_xy[:, 0] = max_inds % feat_width
        max_inds_xy[:, 1] = max_inds // feat_width

        max_deltas_xy = kps_deltas[all_inds, :, max_inds]

        if self.do_pixel:
            kps_pos_distance_x = self.kps_pos_distance_x / self.kps_feat_stride
            kps_pos_distance_y = self.kps_pos_distance_y / self.kps_feat_stride
            max_deltas_xy[:, 0] *= kps_pos_distance_x
            max_deltas_xy[:, 1] *= kps_pos_distance_y
        pred_kps = (max_inds_xy + max_deltas_xy) / scales_xy + origin_xy

        kps_results = np.hstack((pred_kps, max_scores.reshape((-1, 1))))
        kps_results = kps_results.reshape((num_boxes, -1))
        return kps_results
