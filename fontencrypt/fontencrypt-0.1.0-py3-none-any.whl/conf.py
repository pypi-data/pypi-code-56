__author__ = "gdream@126.com"
__author_url__ = "https://ggdream.github.io"
import random

class Glyph:
    def __init__(self, glyphNames: list = None):
        self.__base_glyph_name = ['.notdef']
        self.__default_glyph_names =  ['zero', 'one', 'two', 'three','four', 'five', 'six', 'seven', 'eight', 'nine']

        self.glyph_names = self.__base_glyph_name + (glyphNames if glyphNames != None else self.__default_glyph_names)
        self.rand_names = self.__base_glyph_name + random.sample(self.glyph_names[1:], len(self.glyph_names[1:]))



def NameStrings(familyName: str = "Font", styleName: str = None, author: str = __author__, version: str = "v1.0.0", vendorURL: str = __author_url__) -> dict:
    return {
        "familyName": familyName,
        "styleName": styleName if styleName != None else "enNormal",
        "psName": "-".join((familyName, styleName if styleName != None else "enNormal")),
        "copyright": f"Created by {author}",
        "version": version,
        "vendorURL": vendorURL,
    }