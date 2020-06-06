import os
import platform
import json


def mkdir(*args):
    for folder in args:
        if not os.path.isdir(folder):
            os.makedirs(folder)


def make_join(*args):
    folder = os.path.join(*args)
    mkdir(folder)
    return folder


def list_dir(folder, condition=None, key=lambda x: x, reverse=False):
    files = os.listdir(folder)
    if condition is not None:
        files = filter(condition, files)
    if key is not None:
        files = sorted(files, key=key, reverse=reverse)
    files = [(file, os.path.join(folder, file)) for file in files]
    return files


def flatten(l):
    return [item for sublist in l for item in sublist]


def is_win():
    return platform.system() == "Windows"


def get_postfix(post_fix):
    return lambda x: x.endswith(post_fix)


def partition(images, size):
    """
    Returns a new list with elements
    of which is a list of certain size.

        >>> partition([1, 2, 3, 4], 3)
        [[1, 2, 3], [4]]
    """
    return [
        images[i : i + size] if i + size <= len(images) else images[i:]
        for i in range(0, len(images), size)
    ]


def load_json(file):
    with open(file, "r") as f:
        res = json.load(f)
    return res


def save_json(file, obj):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)
