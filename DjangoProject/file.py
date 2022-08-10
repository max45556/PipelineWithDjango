from my_lib import Object3
from my_lib import Object2
import sys
from third_party import (
    lib15,
    lib1,
    lib2,
    lib3,
    lib4,
    lib5,
    lib6,
    lib7,
    lib8,
    lib9,
    lib10,
    lib11,
    lib12,
    lib13,
    lib14,
)
import sys

keys_list = ["A", "B", "C"]
values_list = ["blue", "red", "bold"]

dict_method_1 = dict(zip(keys_list, values_list))

dict_method_2 = {key: value for key, value in zip(keys_list, values_list)}

items_tuples = zip(keys_list, values_list)
dict_method_3 = {}
for key, value in items_tuples:
    if key in dict_method_3:
        pass  # To avoid repeating keys.
    else:
        dict_method_3[key] = value
