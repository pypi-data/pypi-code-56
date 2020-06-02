import PIL.ImageFont


__ALL__ = "text_with_padding"


def text_with_padding(font: PIL.ImageFont.FreeTypeFont, text: str, padding: int = -1) -> tuple:
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
    height = ascent+descent
    if padding > 0:
        padding = (padding, padding)
    else:
        padding = (offset_y+descent, descent-offset_y)
    shape = (width+padding[0], height+padding[1])
    pos = (padding[0]/2, padding[1])
    return (shape, pos)
