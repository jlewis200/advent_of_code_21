#!/usr/bin/python3

import numpy as np

from code import interact

file_name = "input"
#file_name = "test_data"

def get_fuel(dist):
    return (dist * (dist + 1)) / 2

with open(file_name, "r") as in_file:
    data = np.asarray(in_file.read().strip().split(','), np.int64)
    mean = int(data.mean())

    for mean in range(mean - 3, mean + 2):
        min_fuel = 0
        abs_diff = np.absolute(data - mean)
        min_fuel = np.vectorize(get_fuel)(abs_diff).sum()
        print(min_fuel)
    interact(local=locals())

