from collections import defaultdict

def deepIterate(d):
    for key in d:
        if isinstance(d[key], dict):
            for rest, value in deepIterate(d[key]):
                yield (key, *rest), value
        else:
            yield (key, d[key])

def deepGet(d, path):
    for part in path:
        d = d[part]
    return d

def destructureDict(attrs):
    ret = defaultdict(dict)
    for attr, value in attrs.items():
        if '.' in attr:
            key = attr[:attr.index(".")]
            rest = attr[attr.index(".") + 1:]
            ret[key].update(destructureDict({rest: value}))
        else:
            ret[attr] = value
    return ret