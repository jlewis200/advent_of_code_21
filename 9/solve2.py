#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

h_map = list()


def comp(h_map, rdx, cdx, rdx_, cdx_, discard_nine=False):
    res = True

  
    if not (cdx < h_map.shape[1] and cdx >= 0 and rdx < h_map.shape[0] and rdx >= 0):
        res = False
    
    elif discard_nine and not (cdx_ < h_map.shape[1] and cdx_ >= 0 and rdx_ < h_map.shape[0] and rdx_ >= 0):
        res = False
    
    elif cdx_ < h_map.shape[1] and cdx_ >= 0 and rdx_ < h_map.shape[0] and rdx_ >= 0:
        res = h_map[rdx, cdx] < h_map[rdx_, cdx_]
        
        if discard_nine and h_map[rdx_, cdx_] > 8:
            res = False

    return res

with open(file_name, "rt") as in_file:
    data = in_file.read().split()
    
    for line in data:
        h_map.append(list())
        
        for char in line:
            h_map[-1].append(int(char))

    h_map = np.asarray(h_map)

    basins = list()
    score = 0

    for rdx in range(h_map.shape[0]):
        for cdx in range(h_map.shape[1]):


            #up
            rdx_0 = rdx - 1
            cdx_0 = cdx 

            #left
            rdx_1 = rdx 
            cdx_1 = cdx - 1

            #down
            rdx_2 = rdx + 1
            cdx_2 = cdx

            #right
            rdx_3 = rdx 
            cdx_3 = cdx + 1

            res = comp(h_map, rdx, cdx, rdx_0, cdx_0) and \
                  comp(h_map, rdx, cdx, rdx_1, cdx_1) and \
                  comp(h_map, rdx, cdx, rdx_2, cdx_2) and \
                  comp(h_map, rdx, cdx, rdx_3, cdx_3) 

            if res:
                basins.append((rdx, cdx))


    scores = list()
    for basin in basins:

        basin_coords_todo = set() #coords to check
        basin_coords_comp = set() #complete coords

        basin_coords_todo.add(basin)

        while len(basin_coords_todo) != 0:          
            rdx, cdx = basin_coords_todo.pop()
            basin_coords_comp.add((rdx, cdx))

            #up
            rdx_ = rdx - 1
            cdx_ = cdx 
          
            if comp(h_map, rdx, cdx, rdx_, cdx_, discard_nine=True):
                if (rdx_, cdx_) not in basin_coords_comp:
                    basin_coords_todo.add((rdx_, cdx_))

            #left
            rdx_ = rdx
            cdx_ = cdx - 1 
          
            if comp(h_map, rdx, cdx, rdx_, cdx_, discard_nine=True):
                if (rdx_, cdx_) not in basin_coords_comp:
                    basin_coords_todo.add((rdx_, cdx_))

            #down
            rdx_ = rdx + 1
            cdx_ = cdx 
          
            if comp(h_map, rdx, cdx, rdx_, cdx_, discard_nine=True):
                if (rdx_, cdx_) not in basin_coords_comp:
                    basin_coords_todo.add((rdx_, cdx_))

            #right
            rdx_ = rdx
            cdx_ = cdx + 1
          
            if comp(h_map, rdx, cdx, rdx_, cdx_, discard_nine=True):
                if (rdx_, cdx_) not in basin_coords_comp:
                    basin_coords_todo.add((rdx_, cdx_))


        scores.append(len(basin_coords_comp))
        print("basin size:  %d" % len(basin_coords_comp))

    scores = np.asarray(scores)
    scores.sort()
    scores = scores[-3:]

    interact(local=locals())
    total = 1
    for score in scores:
        total *= score


    print(total)
