#!/usr/bin/python3

import numpy as np
from multiprocessing import Pool
from os import cpu_count
from code import interact

def get_data():
    file_name = "input"
    file_name = "test_data2"
    
    with open(file_name, "r") as in_file:
        actions = list()
    
        for line in in_file:
            action, line = line.strip().split(' ')
            x_rng, y_rng, z_rng = line.split(',')
            
            x_rng = x_rng[2:].split("..")
            y_rng = y_rng[2:].split("..")
            z_rng = z_rng[2:].split("..")
    
            action = 1 if action == "on" else 0
            x_rng = (int(x_rng[0]), int(x_rng[1]))
            y_rng = (int(y_rng[0]), int(y_rng[1]))
            z_rng = (int(z_rng[0]), int(z_rng[1]))
        
            actions.append((action, *x_rng, *y_rng, *z_rng))
    
        actions = np.asarray(actions, dtype=np.int64)

        x_min = actions[:, 1:3].min()
        y_min = actions[:, 3:5].min()
        z_min = actions[:, 5:7].min()
   
        actions[:, 1:3] = actions[:, 1:3] - x_min
        actions[:, 3:5] = actions[:, 3:5] - y_min
        actions[:, 5:7] = actions[:, 5:7] - z_min

        return actions

def sum_intervals(intervals):

    sum = 0
    
    for interval in intervals:
        x = interval[1] - interval[0]
        y = interval[3] - interval[2]
        area = x * y
        
        sum += area if ((x > 0) and (y > 0)) else 0

    return sum

def add_interval(inters, action, x0, x1, y0, y1):

    x1 = x1 + 1
    y1 = y1 + 1

    new_inter = [x0, x1, y0, y1]
    new_inters = [new_inter]
    
    split_intervals(inters, new_inter)

    for inter in inters:
        split_intervals(new_inters, inter)

#    print(inters)
#    print(new_inters)

    if action == 0:
        for new_inter in new_inters:
            if new_inter in inters:
                inters.remove(new_inter)

    elif action == 1:
        for new_inter in new_inters:
            if new_inter not in inters:
                inters.append(new_inter)

def split_intervals(inters, split_inter):
    idx = 0

    x0 = split_inter[0]
    x1 = split_inter[1]
    y0 = split_inter[2]
    y1 = split_inter[3]

    while idx < len(inters):
        inter = inters[idx]

        #vertical split
        if x0 > inter[0] and x0 < inter[1]: 
            inters.append([x0, inter[1], inter[2], inter[3]])
            inter[1] = x0

        #vertical split
        if x1 > inter[0] and x1 < inter[1]:
            inters.append([x1, inter[1], inter[2], inter[3]])
            inter[1] = x1
        
        #horizontal split
        if y0 > inter[2] and y0 < inter[3]: 
            inters.append([inter[0], inter[1], y0, inter[3]])
            inter[3] = y0

        #horizontal split
        if y1 > inter[2] and y1 < inter[3]: 
            inters.append([inter[0], inter[1], y1, inter[3]])
            inter[3] = y1
        
        idx += 1

def get_line_sum(z):
    print(z)
    intervals = []
    
    for action in actions:

        if z >= action[5] and z <= action[6]:
            add_interval(intervals, *action[0:5])

    return sum_intervals(intervals)


actions = get_data()
z_max = actions[:, 5:7].max() + 1

with Pool(max(2, cpu_count() - 2)) as pool:
    line_sums = pool.map(get_line_sum, range(z_max))
    print(sum(line_sums))


#sum = 0
#
#for z in range(z_max):
#    print("%d / %d" %(z, z_max))
#    sum += get_line_sum(z)
#
#print(sum)

#interact(local=locals())
