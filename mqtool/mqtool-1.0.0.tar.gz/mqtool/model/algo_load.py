import importlib
import os

# ignore_files = ['model_service.py','demo.py','__init__.py']
ignore_files = ['model_service.py','__init__.py']

def load_dir(path):
    algo_list = []
    dirs = os.listdir(path)
    for file in dirs:
        if file.endswith('.py') and not file in ignore_files:
            mol = load_source(file[0:len(file) - 3], path + '/' + file)
            # algo_map[file.name] =mol
            if hasattr(mol,'run'):
                algo_list.append(mol)
    return algo_list


def load_source(name, path):
    return importlib.machinery.SourceFileLoader(name, path).load_module()
