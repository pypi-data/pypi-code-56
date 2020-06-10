
import os

IS_POSIX = os.name == 'posix'


#colors
COLOR_BG_NO = 0
COLOR_BG_BLACK = 40
COLOR_BG_RED = 41
COLOR_BG_GREEN = 42
COLOR_BG_YELLOW = 43
COLOR_BG_BLUE = 44
COLOR_BG_FUCHSIA = 45
COLOR_BG_CYAN = 46
COLOR_BG_WHITE = 47

COLOR_TX_BLACK = 30
COLOR_TX_RED = 31
COLOR_TX_GREEN = 32
COLOR_TX_YELLOW = 33
COLOR_TX_BLUE = 34
COLOR_TX_FUCHSIA = 35
COLOR_TX_CYAN = 36
COLOR_TX_WHITE = 37


def color(text :str, col_t, col_b :int=0) -> str:
    if not IS_POSIX:
        return text

    return '\033[%s;%sm%s\033[0m' % (col_b, col_t, text)
