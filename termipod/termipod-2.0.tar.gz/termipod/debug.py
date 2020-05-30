from inspect import currentframe, getframeinfo
from pprint import pprint


def debug(tty, msg):
    frameinfo = getframeinfo(currentframe().f_back)
    print(f'# {frameinfo.filename}:{frameinfo.lineno}',
          file=open(f'/dev/pts/{tty}', 'w'))
    pprint(msg, open(f'/dev/pts/{tty}', 'w'))
