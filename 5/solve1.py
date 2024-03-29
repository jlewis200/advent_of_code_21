#!/usr/bin/python3

import numpy as np
from ast import literal_eval as make_tuple
from code import interact

file_name = "input"
#file_name = "test_data"

with open(file_name, "r") as in_file:
    data = in_file.read().split('\n')[:-1]

    lines = list()
    for line in data:
        src, dst = line.split("->")
        src = make_tuple(src.strip())
        dst = make_tuple(dst.strip())
        
        lines.append((src, dst))
    
    lines = np.asarray(lines)

    xsz = lines[:, :, 0].max() + 1
    ysz = lines[:, :, 1].max() + 1
    grid = np.zeros(shape=(xsz, ysz))

    for line in lines:

        #horizontal line
        if line[0, 0] == line[1, 0]:
            print(line)
            x = line[0, 0]
            y0 = min(line[0, 1], line[1, 1])
            y1 = max(line[0, 1], line[1, 1]) + 1

            grid[x, y0:y1] += 1

        #vertical
        elif line[0, 1] == line[1, 1]:
            print(line)
            y = line[0, 1]
            x0 = min(line[0, 0], line[1, 0])
            x1 = max(line[0, 0], line[1, 0]) + 1

            grid[x0:x1, y] += 1

        #diagonal
        else:
            print("diagonal")
            print(line)
            x0 = line[0, 0]
            x1 = line[1, 0] 
            y0 = line[0, 1]
            y1 = line[1, 1]

            if x0 > x1:
                tmp = x0
                x0 = x1
                x1 = tmp
                tmp = y0
                y0 = y1
                y1 = tmp
            
            x1 += 1
            y1 += 1

            #increasing slope
            if y1 > y0:
                for idx in range(x1 - x0):
                    grid[x0 + idx, y0 + idx] += 1
            
            else:
                for idx in range(x1 - x0):
                    grid[x0 + idx, y0 - idx] += 1


    print(grid[grid > 1].shape[0])
            
    interact(local=locals())
    
