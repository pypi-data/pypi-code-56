import cProfile
from functools import partial, wraps


def profile(func=None, sort="cumtime"):

    if not func:
        return partial(profile, sort)

    pr = cProfile.Profile()

    @wraps(func)
    def wrapper(*args, **kwargs):
        pr.enable()
        ret = func(*args, **kwargs)
        pr.disable()
        pr.print_stats(sort)
        return ret

    return wrapper
