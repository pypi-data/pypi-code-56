import cv2
import numpy as np
from tools.rgb_utils import *
from tools.utils import *


def get_major_color(image, except_colors=[], color_upper=np.array([255, 255, 255]), color_lower=np.array([0, 0, 0])):
    '''
    提取图片中主要颜色
    :param image: 图片
    :param except_colors: 排除色，一般为背景色，需要过滤
    :param color_lower:
    :param color_upper:
    :return: 主色
    '''

    except_str_colors = colors_to_strings(except_colors)
    except_str_colors = set(except_str_colors)

    r, g, b = -1, -1, -1
    r_count, g_count, b_count = 0, 0, 0
    for x in image:
        for y in x:
            str_col = color_to_string(y)
            if str_col in except_str_colors:
                continue

            if (y > color_upper).all():
                continue

            if (y < color_lower).all():
                continue

            if r_count == 0 and g_count == 0 and b_count == 0:
                b = y[0]
                g = y[1]
                r = y[2]

                b_count += 1
                g_count += 1
                r_count += 1
            elif b == y[0] and g == y[1] and r == y[2]:
                b_count += 1
                g_count += 1
                r_count += 1
            else:
                b_count -= 1
                g_count -= 1
                r_count -= 1

    return np.array([b, g, r])


def get_colors_and_counts(img, except_colors=[], color_lower=np.array([0, 0, 0]), color_upper=np.array([255, 255, 255])):
    '''
    统计每个色值在图像中出现的次数
    :param img: 图像
    :param except_colors: 排除颜色
    :param color_upper: 颜色上限
    :param color_lower: 颜色下限
    :return: 色值统计量
    '''

    except_str_colors = colors_to_strings(except_colors)
    except_str_colors = set(except_str_colors)

    unique_colors = dict()
    for x in img:
        for y in x:
            str_col = color_to_string(y)
            if str_col in except_str_colors:
                continue

            if (y > color_upper).all():
                continue

            if (y < color_lower).all():
                continue

            if str_col not in unique_colors.keys():
                unique_colors[str_col] = 0

            unique_colors[str_col] += 1

    return unique_colors


def get_top_right_corder_color(image):
    '''
    提取右上角颜色
    :param image:
    :return:
    '''

    h, w = image.shape[0], image.shape[1]

    sect_w = 3
    sect_h = 3
    right_top_sect = image[:sect_h, w-sect_w:]

    return get_major_color(right_top_sect)


def detect_border(image, color_name):
    '''
    图片切割后，不一定所有的切片都满足要求。一般来说，正好被边框包围，且四周仍保留边框的，才是所需切片。
    :param image: 需要切片的文件
    :param color_name: 切割时采用的边框颜色
    :return: 如果是满足需求的切面，则True；不满足则False
    '''

    # 切片周边2个像素区域，默认认为是边框区域
    thick = 2
    top = image[:thick, :]
    left = image[:, :thick]
    right = image[:, -thick:]
    bottom = image[-thick:, :]

    # 统计切边四周像素中，符合给定边框color的像素点
    count = 0
    for border in (top, left, right, bottom):
        for x in border:
            for y in x:
                if (HSV_RANGES[color_name][0]['lower'] <= y).all() and (y <= HSV_RANGES[color_name][0]['upper']).all():
                    count += 1

    # 求顶部边框与左边边框的像素点个数
    thre = (top.shape[0] * top.shape[1] + left.shape[0] * left.shape[1])

    # 如果四周边框中，符合给定边框color的像素点个数超过一定像素点个数，则返回True，否则False

    if count < thre * 0.8:
        return False

    return True


def remove_invalid_contours(img, rects):
    '''
    删除无效边框
    :param img: 图片矩阵
    :param rects: 轮廓坐标
    :return: 有效边框，矩阵形式
    '''

    color_hashes = set()

    unique_colors = list()
    valid_contours = list()

    # 遍历所有轮廓
    for rect in rects:
        x, y, w, h = rect
        if w * h < 100:
            continue

        # 将边框内的像素切片
        padding = 8
        cropped = img[y + padding:y + h - padding, x + padding:x + w - padding]
        if len(cropped) == 0 or len(cropped[0]) == 0:
            continue

        # 提取右上角主色
        color = get_top_right_corder_color(cropped)

        # 如果右上角为白色，则无效
        if (color >= np.array([250, 250, 250])).all():
            continue

        if color.tostring() in color_hashes:
            continue

        color_hashes.add(color.tostring())

        unique_colors.append(color)
        valid_contours.append(cropped)

    return unique_colors, valid_contours


def get_border_colors_from_template(template_file, n=3):
    '''
    提取给顶边框模板中所有边框颜色，要求背景色为白色。
    :param template_file: 模板文件
    :param n: 每个边框提取的色值数
    :return: 每个边框上出现频率最高的n个色值
    '''

    out_dir = 'tmp/'

    img = cv2.imread(template_file)

    padding = 1
    img1 = img[padding:-padding, padding:-padding]

    # 变成灰度图
    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(out_dir + 'gray-img.png', img2)

    # 变成二值图，0~252 是 0 黑色， > 252是 1 白色
    _, img3 = cv2.threshold(img2, 252, 255, cv2.THRESH_BINARY)
    cv2.imwrite(out_dir + 'binary-img.png', img3)

    # 查找模板文件中所有边框
    contours, hierarchy = cv2.findContours(img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    all_rects = [cv2.boundingRect(cnt) for cnt in contours]

    unique_str_colors = set()
    for idx, rect in enumerate(all_rects):
        x, y, w, h = rect
        if w * h < 100:
            continue

        # 依据边框左上角点的坐标和宽高，将边框内的像素切片
        padding = 1
        cropped = img[y + padding:y + h - padding, x + padding:x + w - padding]
        if len(cropped) == 0:  # or len(cropped[0]) == 0:
            continue

        # 统计每个色值在图像中出现的次数
        colors = get_colors_and_counts(cropped, [], np.array([0, 0, 0]), np.array([200, 200, 200]))

        # 根据色值出现频率排序
        colors = sort_dict(colors, True)

        if len(colors) == 0:
            continue

        # 提取图像中出现频率前n的色值
        for i in range(n):
            unique_str_colors.add(colors[i][0])

    # 去除重复
    unique_colors = []
    for usc in unique_str_colors:
        unique_colors.append(string_to_color(usc))

    return unique_colors


def get_border_colors_from_template2(template_file):
    '''
    提取给顶边框模板中所有边框颜色，要求背景色为白色
    :param template_file: 模板文件
    :return: 所有边框颜色
    '''

    out_dir = 'tmp/'

    img = cv2.imread(template_file)

    padding = 1
    img1 = img[padding:-padding, padding:-padding]

    # 变成灰度图
    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(out_dir + 'img2.png', img2)

    # 变成黑白图
    _, img3 = cv2.threshold(img2, 252, 255, cv2.THRESH_BINARY)
    cv2.imwrite(out_dir + 'img3.png', img3)

    # 查找模板文件中所有边框
    contours, hierarchy = cv2.findContours(img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    all_rects = [cv2.boundingRect(cnt) for cnt in contours]

    unique_colors, valid_contours = remove_invalid_contours(img, all_rects)

    for idx, rect in enumerate(valid_contours):
        # 如果切片中检测到给定的颜色，则判断是所需切片
        cv2.imwrite('%s/detected-borders-%d.png' % (out_dir, idx), rect)

    return unique_colors


def check_irregular_shape(img):
    '''
    检查不规则形状
    :param img: 图像
    :return: 是否为不规则图像
    '''

    prop = img.shape[0] * 1.0 / img.shape[1]

    return prop > 20 or prop < 0.05