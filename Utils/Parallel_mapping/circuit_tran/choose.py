from collections import OrderedDict
from itertools import *
def unique_everseen(iterable, key=None):
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

# lst = [[1,2],[1,3],[1,4],[2,1],[2,5],[3,1],[3,2]]
# lst = list(unique_everseen(lst, key=frozenset))
# print(lst)