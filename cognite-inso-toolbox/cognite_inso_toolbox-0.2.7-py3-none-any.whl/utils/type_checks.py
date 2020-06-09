def is_int(x):
    """
    In the spirit of dynamic typing:
    Any input that can be interpreted/represented as an integer will return True.
    """
    try:
        return float(x) == int(float(x))
    except (ValueError, TypeError):
        return False
