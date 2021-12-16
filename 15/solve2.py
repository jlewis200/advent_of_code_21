#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

def update(weight, path, complete, prev, idx, jdx, idx_, jdx_):
    res = False

    if idx_ >= 0 and \
       idx_ < weight.shape[0] and \
       jdx_ >= 0 and \
       jdx_ < weight.shape[1] and \
       not complete[idx_, jdx_]:

        tent_path = path[idx, jdx] + weight[idx_, jdx_]
        if tent_path < path[idx_, jdx_]:
            path[idx_, jdx_] = tent_path
            prev[idx_, jdx_] = (idx, jdx)
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
    tile_shape = weight.shape
    weight = np.tile(weight, (5, 5))

    #increment tiles along x axis
    for idx in range(1, 5):
        weight[idx * tile_shape[0]:, 0:] += 1

    #increment tiles along y axis
    for idx in range(1, 5):
        weight[0:, idx * tile_shape[1]:] += 1

    #wrap around if greater than 9
    weight[weight > 9] -= 9

    complete = np.full(shape=weight.shape, fill_value=False)
    prev = np.zeros(shape=(weight.shape[0], weight.shape[1], 2), dtype=np.int64)
    path = np.full(shape=weight.shape, fill_value=np.inf)
    path[0, 0] = 0

    nodes = [(path[0, 0], (0, 0))] 

    while not complete[-1, -1] and len(nodes) > 0:
#        print(len(nodes))
        nodes.sort(key=sort_f)
        coord = nodes.pop(0)[1]

        coords_ = [(coord[0] - 1, coord[1]), 
                   (coord[0] + 1, coord[1]), 
                   (coord[0], coord[1] - 1), 
                   (coord[0], coord[1] + 1)]

        for coord_ in coords_: 
            if update(weight, path, complete, prev, *coord, *coord_):
                nodes.append((path[coord_], coord_))
        
        complete[coord] = True

    coord = (-1, -1)
    shortest_path = [(coord)]
    while coord != (0, 0):
        coord = tuple(prev[coord])
        shortest_path.insert(0, coord)

    print(path[-1 ,-1])
