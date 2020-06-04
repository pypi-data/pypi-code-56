#!/usr/bin/env python

"""Tests the ImageDataTest class"""

import torch
from torch.utils import data
import numpy as np

from saliency_detector.dataset.joint_dataset import ImageDataTest


def test_imagedatatest(config):
    """Sample pytest test function with the pytest fixture as an argument."""
    dataset = ImageDataTest(config.image_paths)
    data_loader = data.DataLoader(dataset=dataset, batch_size=config.batch_size, shuffle=False,
                                  num_workers=config.num_thread, pin_memory=False)
    for image_name_size in data_loader:
        image, name, im_size = image_name_size['image'],\
                                image_name_size['name'][0],\
                                np.asarray(image_name_size['size'])
        assert isinstance(image, torch.Tensor)
        assert isinstance(name, str)
        assert isinstance(im_size, np.ndarray)

