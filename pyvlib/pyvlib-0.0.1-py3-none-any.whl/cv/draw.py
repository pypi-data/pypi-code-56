# -*- coding: utf-8 -*-
# @Filename: draw.py
# @Date: 2018-10-25
# @Update: 2020-05-28
# @Author: liwei

import os
import numpy as np
import cv2


def draw_points(img, points, color, size=6, copy=True):
    image = np.array(img, copy=copy)
    row, col = image.shape[:2]
    for p in points:
        x = int(p[0])
        y = int(p[1])
        if x < 0 or y < 0 or x > col-1 or y > row-1:
            raise ValueError(
                'point (%d,%d) outside image with size (%d,%d)' % (x, y, col, row))
        cv2.circle(image, (x, y), size, color, -1)
    return image


def draw_lines(img, pointsA, pointsB, color, width=2, copy=True):
    image = np.array(img, copy=copy)
    row, col = image.shape[:2]
    for p, q in zip(pointsA, pointsB):
        px = int(p[0])
        py = int(p[1])
        qx = int(q[0])
        qy = int(q[1])
        if px < 0 or py < 0 or px > col-1 or py > row-1:
            raise ValueError(
                'point (%d,%d) outside image with size (%d,%d)' % (px, py, col, row))
        if qx < 0 or qy < 0 or qx > col-1 or qy > row-1:
            raise ValueError(
                'point (%d,%d) outside image with size (%d,%d)' % (qx, qy, col, row))
        cv2.line(image, (px, py), (qx, qy), color, width)
    return image


def draw_rect(img, x, y, w, h, color=(0, 255, 0), size=3):
    image = np.array(img, copy=True)
    row, col = image.shape[:2]
    tl_x = min(max(int(x), 0), col-1)
    tl_y = min(max(int(y), 0), row-1)
    br_x = min(int(x+w), col-1)
    br_y = min(int(y+h), row-1)
    cv2.rectangle(image, (tl_x, tl_y), (br_x, br_y), color, size)
    return image


def draw_skeleton(img, points, parents_index, color, width=2, copy=True):
    image = np.array(img, copy=copy)
    # print(type(points), points.shape)
    # print(parents_index)
    for i in range(1, points.shape[0]):
        parent = parents_index[i]
        # print('son:', i, 'parent:', parent)
        p = points[i]
        q = points[parent, :]
        cv2.line(image, (int(p[0]), int(p[1])),
                 (int(q[0]), int(q[1])), color, width)
    return image


def overlay_image(bg, fg, fg_mask, pos):
    """overlays a foreground image (fg) on top of a background image (bg)
    at location (which are (x,y)-coordinates), 
    allowing for alpha transparency via the foreground mask fg_mask

    Args:
        bg ([type]): [description]
        fg ([type]): [description]
        fg_mask ([type]): [description]
        pos ([type]): [description]

    Returns:
        [type]: [description]
    Refs:
        https://www.pyimagesearch.com/2018/11/05/creating-gifs-with-opencv/
    """

    # grab the foreground spatial dimensions (width and height),
    # then unpack the coordinates tuple (i.e., where in the image
    # the foreground will be placed)
    (sH, sW) = fg.shape[:2]
    (x, y) = pos
    # the overlay should be the same width and height as the input
    # image and be totally blank *except* for the foreground which
    # we add to the overlay via array slicing
    overlay = np.zeros(bg.shape, dtype="uint8")
    overlay[y:y + sH, x:x + sW] = fg
    # the alpha channel, which controls *where* and *how much*
    # transparency a given region has, should also be the same
    # width and height as our input image, but will contain only
    # our foreground mask
    alpha = np.zeros(bg.shape[:2], dtype="uint8")
    alpha[y:y + sH, x:x + sW] = fg_mask
    alpha = np.dstack([alpha] * 3)
    # perform alpha blending to merge the foreground, background,
    # and alpha channel together
    output = alpha_blend(overlay, bg, alpha)
    # return the output image
    return output


def alpha_blend(fg, bg, alpha):
    """convert the foreground, background, and alpha layers from
    unsigned 8-bit integers to floats, making sure to scale the
    alpha layer to the range [0, 1]

    Args:
        fg ([type]): [description]
        bg ([type]): [description]
        alpha ([type]): [description]

    Returns:
        [type]: [description]
    Refs:
        https://www.pyimagesearch.com/2018/11/05/creating-gifs-with-opencv/
    """

    fg = fg.astype("float")
    bg = bg.astype("float")
    alpha = alpha.astype("float") / 255
    # perform alpha blending
    fg = cv2.multiply(alpha, fg)
    bg = cv2.multiply(1 - alpha, bg)
    # add the foreground and background to obtain the final output image
    output = cv2.add(fg, bg)

    # return the output image
    return output.astype("uint8")


def test_draw_points():
    file = './data/girl.png'
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    pnts = np.array([10.0, 10.0, 20.0, 20.0])
    pnts = np.reshape(pnts, (-1, 2))
    img_pts = draw_points(img, pnts, [0, 0, 255])
    cv2.imshow('img_pts', img_pts)
    cv2.waitKey()
    # cv2.imwrite(file, img_pts)


if __name__ == "__main__":
    test_draw_points()
