import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

_letter_cases = "abcdefghjkmnpqrstuvwxy"                        # 小写字母
_upper_cases = "ABCDEFGHJKLMNPQRSTUVWXY"                        # 大写字母
_numbers = "1234567890"                                         # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))   # 生成允许的字符集合
default_font = "../font/PingFang.ttc"                               # 验证码字体


# 生成验证码接口
def generate_verify_image(size=(120, 30),
                          chars=init_chars,
                          img_type="GIF",
                          mode="RGB",
                          bg_color=(255, 255, 255),
                          fg_color=(0, 0, 255),
                          font_size=18,
                          font_type=default_font,
                          length=4,
                          draw_lines=True,
                          n_line=(1, 2),
                          draw_points=True,
                          point_chance=2,
                          save_img=False,
                          save_path=None):

    """
    生成验证码图片
    :param size: 图片的大小，格式（宽，高），默认为(120, 30)
    :param chars: 允许的字符集合，格式字符串
    :param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    :param mode: 图片模式，默认为RGB
    :param bg_color: 背景颜色，默认为白色
    :param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    :param font_size: 验证码字体大小
    :param font_type: 验证码字体，默认为 DejaVuSans.ttf
    :param length: 验证码字符个数
    :param draw_lines: 是否划干扰线
    :param n_line: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    :param draw_points: 是否画干扰点
    :param point_chance: 干扰点出现的概率，大小范围[0, 100]
    :param save_img: 是否保存为图片
    :return: [0]: 验证码字节流, [1]: 验证码图片中的字符串
    """

    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""

        return random.sample(chars, length)

    def create_lines():
        """绘制干扰线"""

        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """绘制干扰点"""

        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """绘制验证码字符"""

        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    mstream = io.BytesIO()
    img.save(mstream, img_type)

    if save_img and save_path:
        img.save(save_path, img_type)

    return mstream, strs


if __name__ == "__main__":
    mstream, strs = generate_verify_image(save_img=True)
    print(strs)

#     注意：返回的流要进行转换，在返回前端


# self.write(simplejson.dumps({'code': 0, 'img': stream.getvalue().encode('base64')}))
# #这里是将stream的值进行了一次base64的编码
# 前端js设置图片src代码
# <img src="data:image/jpeg;base64,{{ img_data }}" alt="img_data"  id="imgslot"/>
# $("#verify_code_img").attr("src", "data:image/gif;base64," + data.img);

# 作者：翼动晴空
# 链接：https://www.jianshu.com/p/7b39db561e75
# 来源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。