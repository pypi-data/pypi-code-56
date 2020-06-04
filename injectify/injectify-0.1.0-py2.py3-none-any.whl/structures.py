"""
injectify.structures
~~~~~~~~~~~~~~~~~

This module contains the data structures that power Injectify.
"""

from collections import UserList
from typing import Sequence


class listify(UserList):

    def __init__(self, initlist):
        self.data = []

        if initlist is not None:
            if isinstance(initlist, list):
                self.data[:] = initlist
            elif isinstance(initlist, UserList):
                self.data[:] = initlist.data[:]
            elif isinstance(initlist, Sequence):
                self.data = list(initlist)
            else:
                self.data.append(initlist)
