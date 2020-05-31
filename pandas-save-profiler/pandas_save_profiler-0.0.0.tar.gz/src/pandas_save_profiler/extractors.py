import pandas as pd
import inspect

# Notes about dictionary key order from
# https://stackoverflow.com/a/40007169/4512454

# Python 3.7+
# In Python 3.7.0 the insertion-order preservation nature of dict objects
# has been declared to be an official part of the Python language spec.
# Therefore, you can depend on it.

# Python 3.6 (CPython)
# As of Python 3.6, for the CPython implementation of Python,
# dictionaries maintain insertion order by default.
# This is considered an implementation detail though;
# you should still use collections.OrderedDict if you want
# insertion ordering that's guaranteed across other implementations of Python.


def extract_writer_arguments(writer):
    """
    Extracts all arguments from pandas to_ methods.

    >>> extract_writer_arguments('to_pickle')
    """
    method = getattr(pd.DataFrame, writer)
    arguments = list(inspect.signature(method).parameters.keys())

    first = arguments.pop(0)
    if first != 'self':
        raise Exception(f'First parameter in the writer ({writer}) is not "self".')
    return arguments


def extract_writer_path_argument(writer):
    """
    Extracts path argument from pandas to_ methods.
    Argument in position 1 (after self) is currently returned.
    This function is needed to unwrap decorated writers.

    >>> extract_writer_path_argument('to_pickle')
    """
    return extract_writer_arguments(writer)[0]


def extract_reader_arguments(reader):
    """
    Extracts all arguments from pandas read methods.

    >>> extract_reader_arguments('read_pickle')
    """
    method = getattr(pd, reader)
    arguments = list(inspect.signature(method).parameters.keys())
    return arguments


def extract_reader_path_argument(reader):
    """
    Extracts path argument from pandas read methods.
    Argument in position 0 of the reader is currently returned.
    This function is needed to unwrap decorated readers.

    >>> extract_reader_path_argument('read_pickle')
    """
    return extract_reader_arguments(reader)[0]
