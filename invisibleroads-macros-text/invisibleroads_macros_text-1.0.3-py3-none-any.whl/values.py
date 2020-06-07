import sys


# http://stackoverflow.com/a/23085282/192092
CHARACTER_ENCODING = sys.getfilesystemencoding()


def unicode_safely(x):
    try:
        return x.decode(CHARACTER_ENCODING)
    except (AttributeError, UnicodeDecodeError):
        return x
