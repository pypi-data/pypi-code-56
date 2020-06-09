"""An ordered set data structure."""

import collections


class OrderedSet(collections.MutableSet):
    """An OrderedSet is a set that remembers the insertion order of items."""
    def __init__(self, iterable=[]):
        self._items = []
        self._set = set()

        for i in iterable:
            self.add(i)

    def add(self, item):
        """Add an item to the ordered set."""
        if item not in self._set:
            self._items.append(item)
            self._set.add((item, len(self) - 1))

    def update(self, iterable):
        """Update the set with the given iterable sequence.

        The the index of the last item inserted is returned.

        """
        for item in iterable:
            self.add(item)

    def pop(self):
        """Remove and return the last item inserted into the ordered set.

        Raises KeyError if the set is empty.

        """
        if not self._set:
            raise KeyError('Ordered set is empty')

        self._set.remove(self._items[-1])
        self._items = self._items[:-1]

    def discard(self, item):
        """Remove an item. Do not raise an exception if absent."""
        self._set.discard(item)

    def clear(self):
        """Remove all items from the ordered set."""
        self._items = []
        self._set.clear()

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._set

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and self._items == other._items
