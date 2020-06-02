import os


def makedirs(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def print_log(string, logname=''):
    if logname:
        with open(logname, 'a') as myfile:
            myfile.write(string+'\n')
    print(string)


def append_name(basename, specs=[]):
    out = basename
    for spec in specs:
        out += ('_' + str(spec))
    return out