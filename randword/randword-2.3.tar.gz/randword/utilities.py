from pkg_resources import resource_filename


def get_path_to_data_file(folder: str, filename: str) -> str:
    return resource_filename('randword', 'data/') + f'{folder}{filename}.txt'
