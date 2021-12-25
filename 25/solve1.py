#!/usr/bin/python3

import numpy as np
from code import interact

def get_data():
    filename = "input"
#    filename = "test_data"

    lines = list()

    with open(filename, "r") as in_file:

        for line in in_file:
            line = line.replace(".", "0")
            line = line.replace(">", "1")
            line = line.replace("v", "2")

            lines.append(list(line.strip()))

    return np.asarray(lines, dtype=np.int8)

def print_grid(grid):
    char_map = dict()
    char_map[0] = "."
    char_map[1] = ">"
    char_map[2] = "v"

    for idx in range(grid.shape[0]):
        for jdx in range(grid.shape[1]):
            print(char_map[grid[idx, jdx]], end='')
        print()
    print()

grid = get_data()
print_grid(grid)

for itr in range(1, 50000):
    print("itr:  %d" % itr)
    
    moved = False
    tmp = grid.copy()

    for idx in range(grid.shape[0]):
     
        jdx = 0
        while jdx < grid.shape[1] and grid[idx, jdx] != 0:
            jdx += 1
        
        end = jdx
        if end == grid.shape[1]:
            continue

        jdx += 1
        jdx %= grid.shape[1]

        while jdx != end:
            if grid[idx, jdx] == 1 and \
               grid[idx, (jdx + 1) % grid.shape[1]] == 0:
                tmp[idx, jdx] = 0
                tmp[idx, (jdx + 1) % grid.shape[1]] = 1
                moved = True
 
            jdx += 1
            jdx %= grid.shape[1]

    grid = tmp.copy()
#    print_grid(grid)
    for jdx in range(grid.shape[1]):
        
        idx = 0
        while idx < grid.shape[0] and grid[idx, jdx] != 0:
            idx += 1
        
        end = idx
        if end == grid.shape[0]:
            continue

        idx += 1
        idx %= grid.shape[0]

        while idx != end:
            if grid[idx, jdx] == 2 and \
               grid[(idx + 1) % grid.shape[0], jdx] == 0:
                tmp[idx, jdx] = 0
                tmp[(idx + 1) % grid.shape[0], jdx] = 2
                moved = True

            idx += 1
            idx %= grid.shape[0]

    grid = tmp
#    print_grid(grid)

    if not moved:
        break


#interact(local=locals())

