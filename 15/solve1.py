#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

def update(weight, path, idx, jdx, idx_, jdx_):
    res = False

    if idx_ >= 0 and \
       idx_ < weight.shape[0] and \
       jdx_ >= 0 and \
       jdx_ < weight.shape[1]:

        tent_path = path[idx, jdx] + weight[idx_, jdx_]
        if tent_path < path[idx_, jdx_]:
            path[idx_, jdx_] = tent_path
            res = True

    return res
 
def sort_f(node):
    return node[0]

with open(file_name, "r") as in_file:
    weight = list()
    jdx = 0
    for line in in_file:
        weight.append(list(line.strip()))
        jdx += 1

    weight = np.asarray(weight, dtype=np.int64)
    complete = np.full(shape=weight.shape, fill_value=False)
    path = np.full(shape=weight.shape, fill_value=np.inf)
    path[0, 0] = 0

    nodes = [(path[0, 0], (0, 0))] 
    coord = (0, 0)

    while not complete[coord]:
        #update left
        coord_ = (coord[0] - 1, coord[1])

        update(weight, path, *coord, *coord_)

        #update down
        coord_ = (coord[0], coord[1] + 1)
        update(weight, path, *coord, *coord_)

        #update right
        coord_ = (coord[0] + 1, coord[1])
        update(weight, path, *coord, *coord_)

        #update up
        coord_ = (coord[0], coord[1] - 1)
        update(weight, path, *coord, *coord_)
        

        complete[coord] = True
        mask = ~((path != np.inf) &  (complete == False))
        coord = np.unravel_index(np.ma.MaskedArray(path, mask).argmin(), path.shape)
 
    print(path[-1 ,-1])
