import cv2
import numpy as np

HSV_RANGES = {
    # testified
    'red': [
        {
            'lower': np.array([30, 62, 254]),
            'upper': np.array([32, 64, 256])
        }
    ],
    # testified
    'yellow': [
        {
            'lower': np.array([50, 236, 254]),
            'upper': np.array([70, 238, 256])
        }
    ],
    # green is a major color_name
    'green': [
        {
            'lower': np.array([49, 236, 91]),
            'upper': np.array([49, 236, 91])
        }
    ],
    # testified
    'blue': [
        {
            'lower': np.array([251, 192, 0]),
            'upper': np.array([253, 196, 2])
        }
    ],    # testified
    'gray': [
        {
            'lower': np.array([121, 121, 121]),
            'upper': np.array([123, 123, 123])
        }
    ],
    # testified
    'black': [
        {
            'lower': np.array([0, 0, 0]),
            'upper': np.array([2, 2, 2])
        }
    ],
    # testified
    'white': [
        {
            'lower': np.array([254, 254, 254]),
            'upper': np.array([256, 256, 256])
        }
    ],
}


def create_mask(hsv_img, colors):
    """
    创建黑白图，给定颜色为白，其他颜色为黑
    """

    # 初始化一张空白图片
    mask = np.zeros((hsv_img.shape[0], hsv_img.shape[1]), dtype=np.uint8)

    # 将图片中指定的颜色区域转换成白色，其他的区域则变成黑色。
    for color in colors:
        for color_range in HSV_RANGES[color]:
            # noinspection PyUnresolvedReferences
            mask += cv2.inRange(
                hsv_img,
                color_range['lower'],
                color_range['upper']
            )

    return mask


def add_hsv_range(name, color, delta):
    # 指定颜色名称只保留一种颜色
    HSV_RANGES[name] = []

    hsv_color = dict()
    hsv_color['lower'] = color - delta
    hsv_color['upper'] = color + delta

    HSV_RANGES[name].append(hsv_color)

    return True


def create_mask_via_rgb(hsv_img, colors):
    """
    创建黑白图，给定颜色为白，其他颜色为黑
    """

    # 初始化一张空白图片
    mask = np.zeros((hsv_img.shape[0], hsv_img.shape[1]), dtype=np.uint8)

    # 将图片中指定的颜色区域转换成白色，其他的区域则变成黑色。
    for color in colors:
        lower = color - 30
        upper = color + 30
        mask += cv2.inRange(
            hsv_img,
            lower,
            upper
            )

    return mask


def color_to_string(color):
    return '%d-%d-%d' % (color[0], color[1], color[2])


def string_to_color(str_color):
    sc = str_color.split('-')

    return np.array([int(sc[0]), int(sc[1]), int(sc[2])])


def colors_to_strings(colors):
    result = []
    for col in colors:
        result.append(color_to_string(col))

    return result


def strings_to_colors(str_colors):
    colors = []
    for str_col in str_colors:
        colors.append(string_to_color(str_col))

    return colors


def generate_except_colors(col1, col2):
    if col2 > 256:
        col2 = 256

    cols = []
    for colx in range(col1, col2):
        for coly in range(col1, col2):
            for colz in range(col1, col2):
                cols.append(np.array([colx, coly, colz]))

    return cols


def calculate_color_distance(col1, col2):
    dis = 0
    for i in range(3):
        dis += abs(col1[0] - col2[0])

    return dis


def find_similar_colors_by_distance(col1, colors, delta):
    sim_cols = []
    for col in colors:
        if calculate_color_distance(col1, col) < delta:
            sim_cols.append(col)

    return sim_cols


def find_similar_colors_by_range(col1, colors, delta):
    sim_cols = []
    for col in colors:
        if (col >= col1 - delta).all() and (col < col1 + delta).all():
            sim_cols.append(col)

    return sim_cols


def find_similar_str_colors(str_col1, str_colors, method, delta):
    col1 = string_to_color(str_col1)
    colors = strings_to_colors(str_colors)

    if method == 'distance':
        return find_similar_colors_by_distance(col1, colors, delta)

    return find_similar_colors_by_range(col1, colors, delta)
