"""
Pickle Caching - A way for you to save progress during a time-costing project, and pick right up again if you need to stop in the middle.

To run, first import picklecache.Picache.

Next, instantiate a pickle cache class by running mycache = Picache("./path/to/caching/files")

To use the cacher on a function, add a decorator called with the "subgroup" that you want it to appear in (default is '').

Keys are stored as a tuple, (subgroup, picache_key), so keys only have to be distinct for a certain function.

Then, when you call the function, pass in a keyword argument called picache_key, which will be used to differentiate the function calls.

Function calls are automatically sorted based on the function and class that they were in.

@mycache("MyFunction1")
def costly_function():
    time.sleep(1000)
    return 100

"""

from .picklecache import Picache

__version__ = "0.0.1"
__author__ = "Michael Fatemi"