def parse_bool(val, default):
    if not val:
        return default
    if type(val) == bool:
        return val
    if type(val) == str:
        if val.lower() in ["1", "true"]:
            return True
        if val.lower() in ["0", "false"]:
            return False
    raise ValueError(f"{val} can not be interpreted as boolean")
