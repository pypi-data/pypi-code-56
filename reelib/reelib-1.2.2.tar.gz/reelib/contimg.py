import numpy as np
from PIL import Image


def cv2pil(img):
    """OpenCV->PIL"""
    new_img = img.copy()
    if new_img.ndim == 2:  # モノクロ
        pass
    elif new_img.shape[2] == 3:  # カラー
        new_img = new_img[:, :, ::-1]
    elif new_img.shape[2] == 4:  # 透過
        new_img = new_img[:, :, [2, 1, 0, 3]]
    new_img = Image.fromarray(new_img)
    return new_img


def pil2cv(img):
    """PIL->OpenCV"""
    new_img = np.array(img, dtype=np.uint8)
    if new_img.ndim == 2:  # モノクロ
        pass
    elif new_img.shape[2] == 3:  # カラー
        new_img = new_img[:, :, ::-1]
    elif new_img.shape[2] == 4:  # 透過
        new_img = new_img[:, :, [2, 1, 0, 3]]
    return new_img
