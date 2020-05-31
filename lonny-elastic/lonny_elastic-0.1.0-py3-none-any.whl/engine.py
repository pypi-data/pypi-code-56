import re
from .trie import Trie
from .cfg import Configuration

class Engine:
    def __init__(self):
        self._trie = Trie()
        self._entries = dict()
        self._unique_id = 0

    def _clean(self, string):
        return re.sub("\s\s+", " ", string.lower().strip())

    def add(self, value, corpus):
        self._entries[self._unique_id] = value
        words = self._clean(corpus).split(" ")
        words_len = len(words)
        for start_ix in range(words_len):
            for ngram_words in range(1, Configuration.max_ngram_words):
                fragment =  " ".join(words[start_ix:start_ix + ngram_words])
                self._trie.add(fragment, self._unique_id)
        self._unique_id += 1

    def search(self, query):
        query = self._clean(query)
        return [ self._entries[x] for x in set(self._trie.search(query)) ]