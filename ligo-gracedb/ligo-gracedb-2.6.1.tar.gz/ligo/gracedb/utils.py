import re
import six
from functools import wraps

EVENT_PREFIXES = ['G', 'E', 'H', 'M', 'T']
event_prefix_regex = re.compile(r'^({prefixes})\d+'.format(
    prefixes="|".join(EVENT_PREFIXES)))


# Decorator for class methods so that they work for events or superevents
def event_or_superevent(func):
    @wraps(func)
    def inner(self, object_id, *args, **kwargs):
        is_superevent = True
        if event_prefix_regex.match(object_id):
            is_superevent = False
        return func(self, object_id, is_superevent=is_superevent, *args,
                    **kwargs)
    return inner


# Function for checking arguments which can be strings or lists
# If a string, converts to list for ease of processing
def handle_str_or_list_arg(arg, arg_name):
    if arg:
        if isinstance(arg, six.string_types):
            arg = [arg]
        elif isinstance(arg, list):
            pass
        else:
            raise TypeError("{0} arg is {1}, should be str or list"
                            .format(arg_name, type(arg)))
    return arg
