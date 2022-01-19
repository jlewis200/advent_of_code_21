#!/usr/bin/python3

import numpy as np

from code import interact

file_name = "input"
file_name = "test_data"

def get_fuel(dist):
    return (dist * (dist + 1)) / 2

with open(file_name, "r") as in_file:
    data = np.asarray(in_file.read().strip().split(','), np.int64)
    ccp = np.round(data.mean() - 0.5) #crab collection point
    ccp = int(ccp)
    print(ccp)
    print(data.mean() - 0.5)
    interact(local=locals())

    for ccp in range(ccp - 1, ccp + 3):
        abs_diff = np.absolute(data - ccp)
        min_fuel = np.vectorize(get_fuel)(abs_diff).sum()
        print(min_fuel)

