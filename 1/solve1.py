#!/usr/bin/python3

import numpy as np

with open("input", "rt") as in_file:
    data = np.asarray(in_file.read().split(), dtype=np.int64)
    diff = data[1:] - data[:-1]
    print(diff[diff > 0].shape)
