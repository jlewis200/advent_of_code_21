#!/usr/bin/python3

import numpy as np

from code import interact

def get_fuel(dist):
    return (dist * (dist + 1)) / 2

with open("input", "r") as in_file:
    data = np.asarray(in_file.read().strip().split(','), np.int64)
    ccp_0 = np.round(data.mean() - 0.5) #crab collection point
    ccp_1 = np.round(data.mean() + 0.5) #crab collection point

    abs_diff = np.absolute(data - ccp_0)
    min_fuel = np.vectorize(get_fuel)(abs_diff).sum()
    print("%d %d" % (ccp_0, min_fuel))

    abs_diff = np.absolute(data - ccp_1)
    min_fuel = np.vectorize(get_fuel)(abs_diff).sum()
    print("%d %d" % (ccp_1, min_fuel))

