import os
import sys
import shutil
from tools.img_utils import *
from tools.rgb_utils import *

sys.path.append('/home/sunnycomes/PycharmProjects/python-image-recognition/')

# 输出目录，用于保存切割后的图片
out_dir = 'cropped/'
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.mkdir(out_dir)

tmp_dir = 'tmp/'
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
os.mkdir(tmp_dir)

cropped_loc = set()


def crop(file, color, color_idx):
    '''
    根据指定的边框颜色，切割给定图片。

    :param file: 需要切割的图片
    :param color: 用于切割图片的边框颜色
    :return: None
    '''

    img1 = cv2.imread(file)

    # 添加一种边框颜色
    color_name = 'border-color_name'
    add_hsv_range(color_name, color, 10)

    # 识别图片中的边框，返回的mask为黑白图，边框为白，其余的全部为黑
    mask = create_mask(img1, [color_name])
    cv2.imwrite('tmp/mask-%d.png' % color_idx, mask)

    # 找出黑白图中边框的位置
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(cnt) for cnt in contours]

    # 遍历所有识别出的边框
    for idx, rect in enumerate(rects):
        x, y, w, h = rect
        area = w * h

        # 面积太小直接忽略
        if area < 2000:
            continue

        # 将边框内的像素切片
        padding = 1
        cropped = img1[y + padding:y + h - padding, x + padding:x + w - padding]
        if len(cropped) == 0 or len(cropped[0]) == 0:
            continue

        # 检查是否为不规则图像
        if check_irregular_shape(cropped):
            continue

        # 如果以x, y作为左上的图像已经经切片，不需要再重复操作
        loc = '%dx%d' % (x, y)
        if loc in cropped_loc:
            continue

        # 如果切片中未检测到给定的颜色，则不是所需切片
        if not detect_border(cropped, color_name):
            continue

        cv2.imwrite('%s/%s-%dx%d.png' % (out_dir, loc, w, h), cropped)

        # 以x, y为基点，周边margin个像素点区域作为已经切片过的区域，不需要重复切片
        margin = 20
        for i in range(x-margin, x+margin):
            for j in range(y-margin, y+margin):
                loc = '%dx%d' % (i, j)
                cropped_loc.add(loc)


def main():
    # 从边框文件中提取边框颜色，要求背景色必须为白色
    colors = get_border_colors_from_template(sys.argv[1])
    for col in colors:
        print(color_to_string(col))

    # 遍历所有边框颜色，进行切片
    for idx, color in enumerate(colors):
        crop(sys.argv[2], color, idx)


if __name__ == '__main__':
    main()


