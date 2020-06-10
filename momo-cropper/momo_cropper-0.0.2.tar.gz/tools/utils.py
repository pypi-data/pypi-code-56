from collections import Counter


def sort_dict(dict_obj, reverse=False):
    c = Counter(dict_obj)
    return c.most_common()

