class Trie:
    def __init__(self):
        self._children = dict()
        self._values = set()

    def _has_node(self, char):
        return char in self._children

    def _get_node(self, char):
        if not self._has_node(char):
            self._children[char] = Trie()
        return self._children[char]

    def add(self, path, value):
        self._values.add(value)
        if len(path) == 0:
            return
        child = self._get_node(path[0])
        child.add(path[1:], value)

    def search(self, path):
        if len(path) == 0:
            return self._values
        if not self._has_node(path[0]):
            return set()
        child = self._get_node(path[0])
        return child.search(path[1:])