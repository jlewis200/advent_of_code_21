#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

h_map = list()


def comp(h_map, rdx, cdx, rdx_, cdx_):
    res = True

    if cdx_ < h_map.shape[1] and cdx_ >= 0 and rdx_ < h_map.shape[0] and rdx_ >= 0:
        res = h_map[rdx, cdx] < h_map[rdx_, cdx_]

    return res

with open(file_name, "rt") as in_file:
    data = in_file.read().split()
    
    for line in data:
        h_map.append(list())
        
        for char in line:
            h_map[-1].append(int(char))

    h_map = np.asarray(h_map)

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
                score += 1 + h_map[rdx, cdx]
                print ("%d %d %d" % (rdx, cdx, h_map[rdx, cdx]))

    print(score)
    interact(local=locals())
