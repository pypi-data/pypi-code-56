def decode_string(s):
    try:
        return s.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        return s


def force_str(s, encoding='utf-8', errors='strict'):
    if issubclass(type(s), str):
        return s
    try:
        if isinstance(s, bytes):
            s = str(s, encoding, errors)
        else:
            s = str(s)
    except UnicodeDecodeError as e:
        raise e
    return s


def get_value_or_none(data, index):
    try:
        return data[index]
    except IndexError:
        return None
