from pathlib import Path
import pytest


@pytest.fixture
def config(image_filepaths):
    """Sample configuration object for Saliency Detector"""
    from saliency_detector import Config
    config = Config(model='results/run-1/models/final.pth', image_paths=image_filepaths)

    return config


@pytest.fixture
def image_filepaths():
    """Sample filepaths for saliency detection"""
    return list(Path('./tests/test_data').glob('*.jpg'))
