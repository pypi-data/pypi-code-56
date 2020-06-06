import numpy as np
import torch
from PIL import Image
from tifffile import imwrite


class Stack:
    def __init__(self):
        self._data = None
    
    def __add__(self, other):
        if isinstance(other, type(self)):
            self._data = self._data + other._data
        else:
            self._data = self._data + other
    
    def __mul__(self, other):
        if isinstance(other, type(self)):
            self._data = self._data * other._data
        else:
            self._data = self._data * other
    
    def open(self, path):
        assert isinstance(path, str), "path need to be string"
        if any(path.split(".")[-1] in s for s in [".tif", ".tiff"]):
            pic = Image.open(path)
            w, h = pic.size
            np_array = np.zeros((w, h, pic.n_frames))
            for i in range(pic.n_frames):
                pic.seek(i)
                np_array[:, :, i] = np.array(pic).astype(np.double).T
            self._data = np_array
        else:
            raise ValueError("Only accept .tif, .tiff files. Check path.")

        return self