import functools
from collections import defaultdict

from src.exceptions import DeadEndException

CACHE_PER_MAP = defaultdict(dict)
SEEN_BUT_NOT_COMPUTED = "SEEN_BUT_NOT_COMPUTED"


def memoize(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        map_, path, *_ = args
        start_path_element = path[-1]
        cache = CACHE_PER_MAP[map_]
        if result := cache.get(start_path_element):
            return result
        # Else
        result = func(*args, **kwargs)
        cache[start_path_element] = result
        return result

    return wrapper
