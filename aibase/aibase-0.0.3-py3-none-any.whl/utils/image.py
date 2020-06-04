# -*- coding: utf-8 -*-
# @Time: 2020/6/3 0003
# @Author: gmo_ye
# @Version: 1.0.0
# @Function: 图片操作
import base64
import io
import re

import numpy as np
from PIL import Image


def b64_to_arr(b64):
    """
        将base64字符串转为arr图片
    :param b64: 图片base64字符串
    :return: np.array 格式图片
    """
    base64_data = re.sub('^data:image/.+;base64,', '', b64)
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    return np.array(img)


def arr_to_b64(arr, format='jpeg'):
    """
        将arr图片转为base64字符串
    :param arr: arr图片
    :param format: 文件格式
    :return: 转为对应格式图片的base64字符串
    """
    arr = Image.fromarray(arr.astype('uint8'))
    output_buffer = io.BytesIO()
    arr.save(output_buffer, format=format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()
    return base64_str


__all__ = ['b64_to_arr', 'arr_to_b64']
