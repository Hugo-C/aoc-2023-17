import functools
from collections import defaultdict

from src.exceptions import DeadEndException

CACHE_PER_MAP = defaultdict(dict)
SEEN_BUT_NOT_COMPUTED = "SEEN_BUT_NOT_COMPUTED"


def memoize(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        map_, start_path_element, *_ = args
        cache = CACHE_PER_MAP[map_]
        if result := cache.get(start_path_element):
            if result == SEEN_BUT_NOT_COMPUTED:
                raise DeadEndException()
            else:
                return result
        # Else
        cache[start_path_element] = SEEN_BUT_NOT_COMPUTED
        try:
            result = func(*args, **kwargs)
        except DeadEndException:
            del cache[start_path_element]  # we hitted a dead end further down the road, but it does not mean this one is a dead end ??
            raise
        else:
            cache[start_path_element] = result
        return result

    return wrapper
