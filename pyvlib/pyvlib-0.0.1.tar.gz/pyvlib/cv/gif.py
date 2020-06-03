# -*- coding: utf-8 -*-
# @Filename: gif.py
# @Date: 2018-10-25
# @Update: 2020-05-28
# @Author: liwei

import os

__all__ = ['create', 'resize', 'optimize']


def create(path, file='movie.gif', fps=30, method='pillow', img_ext='.png'):
    """Create a gif

    Args:
        path (str): Input path of image sequence
        file (str, optional): Output gif file. Defaults to 'movie.gif'.
        fps (int, optional): FPS. Defaults to 30.
        method (str, optional): imageio, pillow. Defaults to 'imageio'.

    Raises:
        ValueError: Unsupport method
    """

    image_file_list = []
    for f in sorted(os.listdir(path)):
        if f.endswith(img_ext):
            fp = os.path.join(path, f)
            # print('Add %3d frame %s' % (len(image_file_list), fp), end='\n')
            image_file_list.append(fp)

    if method is 'imageio':
        _create_with_imageio(image_file_list, file, fps)
    elif method is 'pillow':
        _create_with_pillow(image_file_list, file, fps)
    else:
        raise ValueError('Unsupport method, support imageio, pillow only')


def resize(src_gif, dst_gif, dst_size):
    _resize_using_pillow(src_gif, dst_gif, dst_size)


def optimize():
    pass


def _create_with_imageio(image_file_list, gif_file, fps=30):
    try:
        import imageio
    except ImportError:
        raise ImportError('Failed to import imageio')

    images = []
    for file in image_file_list:
        images.append(imageio.imread(file))

    # Save the images as an animated GIF
    imageio.mimsave(gif_file, images, fps)


def _create_with_pillow(image_file_list, gif_file, fps=30):
    try:
        from PIL import Image
    except ImportError:
        raise ImportError('Failed to import PIL')

    images = []
    for file in image_file_list:
        images.append(Image.open(file))

    # Save the images as an animated GIF
    if len(images) == 1:
        images[0].save(gif_file, format='GIF', optimize=False)
    else:
        images[0].save(gif_file, format='GIF', save_all=True, append_images=images[1:],
                       optimize=False, duration=100, fps=fps, loop=0)


def _resize_using_pillow(src_gif, dst_gif, dst_size):
    try:
        from PIL import Image, ImageSequence
    except ImportError:
        raise ImportError('Failed to import PIL')

    # https://gist.github.com/skywodd/8b68bd9c7af048afcedcea3fb1807966
    im = Image.open(src_gif)
    frames = ImageSequence.Iterator(im)

    frames_resized = []
    for frame in frames:
        frames_resized.append(frame.resize(dst_size, Image.ANTIALIAS))

    om = frames_resized[0]  # Handle first frame separately
    om.info = im.info  # Copy sequence info
    om.save(dst_gif, format='GIF', save_all=True,
            append_images=frames_resized[1:])


def create_image_with_text(image, x, y, text, color=(0, 0, 0)):
    from PIL import Image, ImageFont, ImageDraw
    # https://pythonprogramming.altervista.org/create-an-animated-gif-with-pil/
    fnt = ImageFont.truetype("Arial.ttf", 36)
    draw = ImageDraw.Draw(image)
    # draw.ellipse takes a 4-tuple (x0, y0, x1, y1) where (x0, y0) is the top-left bound of the box
    # and (x1, y1) is the lower-right bound of the box.
    draw.text((x, y), text, font=fnt, fill=color)
    return image


def test():
    def gen_image_seq(path):
        from PIL import Image

        string = "HELLO WORLD..."
        string2 = "HAPPY CODING..."
        width, height = 300, 100
        image = Image.new('RGB', (width, height), "yellow")

        frame = 0
        x, y = 0, 0
        for i in range(len(string)):
            image = create_image_with_text(image, x, y, string[:i])
            image.save(os.path.join(path, 'img{:02d}.png'.format(frame)))
            frame += 1
        for i in range(len(string2)):
            image = create_image_with_text(image, x, y+60, string2[:i])
            image.save(os.path.join(path, 'img{:02d}.png'.format(frame)))
            frame += 1

    path = './data/gif/img_seq'
    gen_image_seq(path)
    create(path, './data/gif/img.gif', 30, 'imageio')
    resize('./data/gif/img.gif', './data/gif/img-resize.gif', (600, 200))


if __name__ == "__main__":
    test()
