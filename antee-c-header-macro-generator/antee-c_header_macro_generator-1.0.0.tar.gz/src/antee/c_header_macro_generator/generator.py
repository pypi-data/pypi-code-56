def get_macro_name(filename):
    upper_name = filename.upper()
    remove_dot = upper_name.replace(".", "_")
    macro_name = "__" + remove_dot + "__"
    return macro_name
