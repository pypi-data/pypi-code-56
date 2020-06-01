import cv2
import matplotlib.pyplot as plt
from .utils import *

def debug_polys(np_image_or_path, polys, BNMode=True, color=255, thickness=1, save_image_path=None):
    
    np_image = imread(np_image_or_path)
    if polys is None: return np_image
    if BNMode:
        zeros_img = np.zeros(np_image.shape[:2])
    else:
        zeros_img = np_image.copy()
    for poly in polys:
        draw = cv2.polylines(zeros_img, [poly.astype('int32')], True, color, thickness)
    # plt.figure(figsize=(15,15))
    # plt.imshow(draw[...,::-1])
    if save_image_path:
        cv2.imwrite(save_image_path, draw)
    return draw