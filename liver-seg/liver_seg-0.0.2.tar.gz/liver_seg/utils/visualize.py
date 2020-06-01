import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def add_colored_dilate(image, mask_image, dilate_image):
    mask_image_gray = cv.cvtColor(mask_image, cv.COLOR_BGR2GRAY)
    dilate_image_gray = cv.cvtColor(dilate_image, cv.COLOR_BGR2GRAY)

    mask = cv.bitwise_and(mask_image, mask_image, mask=mask_image_gray)
    dilate = cv.bitwise_and(dilate_image, dilate_image, mask=dilate_image_gray)

    mask_coord = np.where(mask != [0, 0, 0])
    dilate_coord = np.where(dilate != [0, 0, 0])

    mask[mask_coord[0], mask_coord[1], :] = [255, 0, 0]
    dilate[dilate_coord[0], dilate_coord[1], :] = [0, 0, 255]

    ret = cv.addWeighted(image, 0.7, dilate, 0.3, 0)
    ret = cv.addWeighted(ret, 0.7, mask, 0.3, 0)

    return ret


def add_colored_mask(image, mask_image, mask_alpha=0.25):
    ret = None
    if image.ndim == 2 and mask_image.ndim == 3:
        mask_image_gray = cv.cvtColor(mask_image, cv.COLOR_BGR2GRAY)
        ret = image * (1-mask_alpha) + mask_image_gray * mask_alpha + 0
        # ret = ret.astype(np.uint8)
    # mask = cv.bitwise_and(mask_image, mask_image, mask=mask_image_gray)
    # mask_coord = np.where(mask != [0, 0, 0])
    # mask[mask_coord[0], mask_coord[1], :] = [255, 0, 0]
    # ret = cv.addWeighted(image, 0.7, mask, 0.3, 0)
    return ret


def diff_mask(ref_image, mask_image):
    mask_image_gray = cv.cvtColor(mask_image, cv.COLOR_BGR2GRAY)

    mask = cv.bitwise_and(mask_image, mask_image, mask=mask_image_gray)

    mask_coord = np.where(mask != [0, 0, 0])

    mask[mask_coord[0], mask_coord[1], :] = [255, 0, 0]

    ret = cv.addWeighted(ref_image, 0.7, mask, 0.3, 0)
    return ret


# helper function for data visualization
def visualize(**images):
    """PLot images in one row."""
    n = len(images)
    plt.figure(figsize=(16, 5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image)
    plt.show()
