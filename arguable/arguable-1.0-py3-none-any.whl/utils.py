"""General purpose utility functions."""


def removeprefix(string, prefix):
    if prefix and string.startswith(prefix):
        return string[len(prefix):]
    return string


def removesuffix(string, suffix):
    if suffix and string.endswith(suffix):
        return string[:-len(suffix)]
    return string
