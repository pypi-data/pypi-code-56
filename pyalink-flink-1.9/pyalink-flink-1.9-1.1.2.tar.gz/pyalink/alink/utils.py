from .params import Params


def make_params_from_args(*args, **kwargs):
    if 'params' in kwargs:
        x = kwargs.pop('params', None)
        if isinstance(x, (Params,)):
            params = x
        elif isinstance(x, (dict,)):
            params = Params()
            for k, v in x.items():
                params[k] = v
        else:
            raise TypeError('Invalid type of params')
    else:
        params = Params()

    for idx, x in enumerate(args):
        if isinstance(x, (Params,)):
            for k, v in x.items():
                params[k] = v
        else:
            params['arg_{}'.format(idx)] = x

    for k, v in kwargs.items():
        params[k] = v

    return params


def ensure_unicode(x):
    if isinstance(x, (bytes,)):
        return x.decode('utf-8')
    return x


def has_pyflink() -> bool:
    """
    Test if pyflink is found, i.e. pyalink 1.10+
    :return: pyflink if found or not
    :rtype bool
    """
    try:
        import pkg_resources
        pkg_resources.get_distribution("pyalink-flink-1.9")
    except:
        return True
    return False


def get_alink_lib_path() -> str:
    import pyalink
    import os
    for path in pyalink.__path__:
        lib_path = os.path.join(path, "lib")
        if os.path.isdir(lib_path):
            return lib_path
    raise Exception("Cannot find pyalink Java libraries, please check your installation.")


def get_pyflink_path() -> str:
    if has_pyflink():
        import pyflink
        import os
        for path in pyflink.__path__:
            if os.path.isdir(path):
                return path
    else:
        alink_lib_path = get_alink_lib_path()
        import os
        for f in os.listdir(alink_lib_path):
            path = os.path.join(alink_lib_path, f)
            if f.startswith("flink-") and os.path.isdir(path):
                return path
    print("Warning: cannot find pyflink path. "
          "If not running using 'flink run', please check if PyFlink is installed correctly.")
