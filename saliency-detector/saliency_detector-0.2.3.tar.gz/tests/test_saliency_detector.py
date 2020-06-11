#!/usr/bin/env python

"""Tests the saliency_detector class"""

from PIL import Image
import cv2
import pytest
from saliency_detector import SaliencyDetector


def test_saliency_detector(image_filepaths):
    """Sample pytest test function with the pytest fixture as an argument."""
    # imgs = [Image.open(image_filepath) for image_filepath in image_filepaths[:2]]
    imgs = [cv2.imread(str(path)) for path in image_filepaths[:2]]
    sal_det = SaliencyDetector()#image_filepaths[:2])
    result1 = sal_det.solver.predict(imgs[0])
    result2 = sal_det.solver.predict(imgs[1])

    print('bye')
