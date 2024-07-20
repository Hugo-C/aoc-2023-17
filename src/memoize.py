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
                raise DeadEndException()  # we would get in a loop
            else:
                return result
        # Else
        cache[start_path_element] = SEEN_BUT_NOT_COMPUTED
        try:
            result = func(*args, **kwargs)
        except DeadEndException:
            # clear SEEN_BUT_NOT_COMPUTED status on PathElement that hit a loop
            del cache[start_path_element]
            raise
        else:
            cache[start_path_element] = result
        return result

    return wrapper
