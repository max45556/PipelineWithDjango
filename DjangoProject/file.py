from __future__ import absolute_import

import os
import sys

from my_lib import Object, Object2, Object3
from third_party import (lib1, lib2, lib3, lib4, lib5, lib6, lib7, lib8, lib9,
                         lib10, lib11, lib12, lib13, lib14, lib15)


def sort_by_indexes(lst, indexes, reverse=False):
    return [
        val
        for (_, val) in sorted(zip(indexes, lst), key=lambda x: x[0], reverse=reverse)
    ]


a = ["eggs", "bread", "oranges", "jam", "apples", "milk"]
b = [3, 2, 6, 4, 1, 5]
sort_by_indexes(a, b)  # ['apples', 'bread', 'eggs', 'jam', 'milk', 'oranges']
sort_by_indexes(a, b, True)
# ['oranges', 'milk', 'jam', 'eggs', 'bread', 'apples']
