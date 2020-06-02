from tlr.utils import get_value_or_none


def floatable(v):
    try:
        _ = float(v)
        return True
    except (TypeError, ValueError):
        return False


def format_as_str(data, format_template='{:.2f}'):
    return [format_template.format(d) if floatable(d) else None for d in data]


def list_to_dict(data, keys):
    return dict([
        (k, get_value_or_none(data, i)) for i, k in enumerate(keys)
    ])


def stringify_dict(data, format_template='{:.2f}', keys=None):
    if not data:
        if keys:
            return list_to_dict([], keys)
        return {}
    return {k: format_template.format(v) if floatable(v) else None for k, v in data.items()}
