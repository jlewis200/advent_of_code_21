#!/usr/bin/python3

import numpy as np
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


def add_interval(intervals, action, x0, x1):

    if action == 0:

        for idx in range(len(intervals)):

            if x0 >= intervals[idx][0] and x0 <= intervals[idx][1]:
                right = intervals[idx][1]
                intervals[idx][1] = x0 - 1
                if right >= x1 + 1:
                    intervals.append([x1 + 1, right])
 
            if x1 >= intervals[idx][0] and x0 <= intervals[idx][1]:
                left = intervals[idx][0]
                intervals[idx][0] = x1 + 1
                if x0 - 1 >= left:
                    intervals.append([left, x0 - 1])
            
            if intervals[idx][0] >= x0 and intervals[idx][0] <= x1:
                intervals[idx][0] = x1 + 1

            if intervals[idx][1] >= x0 and intervals[idx][1] <= x1:
                intervals[idx][1] = x0 - 1

    elif action == 1:

        for idx in range(len(intervals)):

            if  (x0 >= intervals[idx][0] and x0 <= intervals[idx][1]) or \
                (intervals[idx][1] >= x0 and intervals[idx][1] <= x1):
                
                x1 = max(x1, intervals[idx][1])
                intervals[idx][1] = x0 - 1

            if  (x1 >= intervals[idx][0] and x1 <= intervals[idx][1]) or \
                (intervals[idx][0] >= x0 and intervals[idx][0] <= x1):

                x0 = min(x0, intervals[idx][0])
                intervals[idx][0] = x1 + 1

        intervals.append([x0, x1])

def sum_intervals(intervals):

    sum = 0
    
    for interval in intervals:
        tmp = (interval[1] - interval[0]) + 1
        sum += tmp if tmp > 0 else 0

    return sum

actions = get_data()

grid = np.full(shape=(101, 101, 101), fill_value=False)

x_max = actions[:, 1:3].max() + 1
y_max = actions[:, 3:5].max() + 1
z_max = actions[:, 5:7].max() + 1

sum = 0

for z in range(z_max + 1):
    print("%d / %d" %(z, z_max))
    for y in range(y_max + 1):
#        y = 35
#        z = 84
        
        intervals = []
        
        for action in actions:

            y_rng = y >= action[3] and y <= action[4]
            z_rng = z >= action[5] and z <= action[6]

            if y_rng and z_rng:
                add_interval(intervals, *action[0:3])

#                print("%3d %3d %3d " % tuple(action[0:3]), end='')
#                print("%5d " % sum_intervals(intervals), end=' ')
#                print(intervals)

        line_sum = sum_intervals(intervals)
#        print("%d %d %d" % (y, z, line_sum))        

        sum += line_sum

#        print(sum)
#        exit()

print(sum)

#interact(local=locals())
