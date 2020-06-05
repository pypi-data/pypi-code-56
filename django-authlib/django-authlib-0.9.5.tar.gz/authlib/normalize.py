import unicodedata


def normalize_email(value):
    if not isinstance(value, str):
        return value

    value = unicodedata.normalize("NFKC", value)
    if hasattr(value, "casefold"):
        value = value.casefold()

    return value
