#!/usr/bin/python3

import numpy as np

with open("input", "r") as in_file:
    data = np.asarray(in_file.read().strip().split(','), np.int64)
    print(np.absolute(data - np.round(np.median(data))).sum())
