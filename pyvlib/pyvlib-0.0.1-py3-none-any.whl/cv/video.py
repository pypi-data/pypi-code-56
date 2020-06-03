# -*- coding: utf-8 -*-
# @Filename: video.py
# @Date: 2018-10-25
# @Update: 2020-05-28
# @Author: liwei

import numpy as np
import cv2


def convert_video_to_images(video, frame_step=1, viz=False):
    """
    convert a video to images list
    Args:
        video: string, video file
        frame_step: frame step size
        viz: whether to visualize images

    Returns:
        images_list: images
    """
    if isinstance(video, str):
        cap = cv2.VideoCapture(video)
    else:
        raise ValueError('wrong input')

    if not cap.isOpened():
        print('failed to open video from file', video)
        exit(-1)
    # print('fps =', cap.get(cv2.CAP_PROP_FPS))
    frame = 0
    images_list = []
    while cv2.waitKey(30) != ord('q'):
        retval, image = cap.read()
        if not retval:
            break

        # image = np.rot90(image, k=3, axes=(0, 1))
        if frame_step > 1 and frame % frame_step != 0:
            frame += 1
            continue
        if viz:
            cv2.imshow("video", image)
        images_list.append(image)
        frame += 1
        # break
    cap.release()
    return images_list


def convert_images_to_video():
    pass


if __name__ == "__main__":
    pass
