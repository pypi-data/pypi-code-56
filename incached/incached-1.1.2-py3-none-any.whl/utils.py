"""Utilities for incached"""
import pickle
from .cache import INCached


def load_full_cache(path: str) -> INCached:
    """Load full-dumped cache from file"""
    with open(path, "rb") as inp:
        return pickle.load(inp)


def save_full_cache(path: str, cache_obj: INCached):
    """Full dump cache to file"""
    with open(path, "wb") as output:
        pickle.dump(cache_obj, output, pickle.HIGHEST_PROTOCOL)
