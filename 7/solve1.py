#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

min_fuel = 0
with open(file_name, "r") as in_file:
    data = np.asarray(in_file.read().strip().split(','), np.int64)
    med = np.round(np.median(data))
    print(np.absolute(data - med).sum())
