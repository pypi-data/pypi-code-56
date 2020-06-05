"""INCached cache"""
import pickle
from typing import Dict, Any, Callable


class INCached:
    """Provides cache for your func"""
    def __init__(self, cachesize: int = 100):
        """
        cachesize - max size of cache, set to 0 for no limits
        """
        self._cache: Dict[tuple, Any] = {}
        self._cachesize: int = cachesize
        self.hits: int = 0
        self.misses: int = 0

    def cache(self, func: Callable, args: tuple):
        """
        func - your function without ()
        args - tuple with args
        """
        try:
            value = self._cache[args]
            self.hits += 1
            return value
        except KeyError:
            self.misses += 1
            if self._cachesize != 0:
                if len(self._cache) >= self._cachesize:
                    return func(*args)
            self._cache[args] = func(*args)
            return self._cache[args]

    def cache_info(self) -> Dict[str, int]:
        """Get cache info"""
        return {"hits": self.hits, "misses": self.misses, "cachesize": len(self._cache)}

    def clear_cache(self):
        """Clear cache"""
        self._cache = {}
        self.hits = 0
        self.misses = 0

    def clear_stats(self):
        """Clear hits and misses"""
        self.hits = 0
        self.misses = 0

    def save_cache(self, path: str, save_stats: bool = False, protocol=pickle.HIGHEST_PROTOCOL):
        """Save cache to file"""
        if save_stats:
            save = (self._cache, self.hits, self.misses)
        else:
            save = (self._cache, 0, 0)
        with open(path, "wb") as output:
            pickle.dump(save, output, protocol)

    def load_cache(self, path: str, load_stats: bool = False):
        """Load cache from file"""
        self.clear_cache()
        with open(path, "rb") as inp:
            self._cache, hits, misses = pickle.load(inp)
            if load_stats:
                self.hits, self.misses = hits, misses
