#!/usr/bin/python3

import numpy as np
from code import interact

with open("input", "rt") as in_file:
#with open("test_data", "rt") as in_file:
    data = np.asarray(in_file.read().split(), dtype=np.int64)
    data = np.lib.stride_tricks.sliding_window_view(data, (3,)).sum(axis=1)
    diff = data[1:] - data[:-1]
    print(diff[diff > 0].shape)
