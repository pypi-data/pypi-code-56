#!/usr/bin/env python

"""Tests the saliency_detector class"""

import pytest
from saliency_detector import SaliencyDetector


def test_saliency_detector(image_filepaths):
    """Sample pytest test function with the pytest fixture as an argument."""
    sal_det = SaliencyDetector(image_filepaths[:2])
    sal_det_iter = iter(sal_det)
    image = next(sal_det_iter)
    image2 = next(sal_det_iter)
    with pytest.raises(StopIteration):
        next(sal_det_iter)
