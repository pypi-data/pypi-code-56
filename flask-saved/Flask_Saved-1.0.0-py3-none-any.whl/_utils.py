import os

def get_file_extension(filename):
    _, ext_name = os.path.splitext(filename)
    return ext_name.lower()[1:]