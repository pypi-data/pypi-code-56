# -*- coding: utf-8 -*-
# @Filename: bbox.py
# @Date: 2020-05-30
# @Update: 2020-05-30
# @Author: liwei

import math
import numpy as np
import cv2


def bbox2d(points):
    """
    compute the bounding box & center of 2d points
    Args:
        points:

    Returns:

    """
    minx, miny = float("inf"), float("inf")
    maxx, maxy = float("-inf"), float("-inf")
    for x, y in points:
        # Set min coords
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        # Set max coords
        if x > maxx:
            maxx = x
        elif y > maxy:
            maxy = y
    cx = minx + (maxx-minx)*0.5
    cy = miny + (maxy-miny)*0.5
    return minx, maxx, miny, maxy, cx, cy


def bbox3d(points):
    """
    compute the bounding box & center of 3d points
    Args:
        points:

    Returns:

    """
    minx, miny, minz = float("inf"), float("inf"), float("inf")
    maxx, maxy, maxz = float("-inf"), float("-inf"), float("-inf")
    for x, y, z in points:
        # Set min coords
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        if z < minz:
            minz = z
        # Set max coords
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y
        if z > maxz:
            maxz = z
    cx = minx + (maxx-minx)*0.5
    cy = miny + (maxy-miny)*0.5
    cz = minz + (maxz-minz)*0.5
    bbox = dict()
    bbox['min'] = np.array([minx, miny, minz])
    bbox['max'] = np.array([maxx, maxy, maxz])
    bbox['center'] = np.array([cx, cy, cz])
    return bbox


if __name__ == "__main__":
    pass
