#!/usr/bin/python3

import numpy as np
from scipy.sparse import lil_matrix, csc_matrix, csr_matrix
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

intervals = list()
a = list()

a.append((1, 2, 8))
a.append((0, 3, 5))
a.append((1, 4, 7))
a.append((1, 7, 9))
a.append((1, 2, 8))

for action in a:
    x0 = action[1]
    x1 = action[2]

    if len(intervals) == 0:
        if action[0] == 1:
            intervals.insert(0, (x0, '['))
            intervals.insert(0, (x1 + 1, ']'))

    else:
        if action[0] == 1:
            for idx in range(len(intervals)):
                if x0 < intervals[idx][0]:
                    intervals.insert(idx, (x0, '['))
                    

actions = get_data()

x_max = actions[:, 1:3].max() + 1
y_max = actions[:, 3:5].max() + 1
z_max = actions[:, 5:7].max() + 1

sum = 0

for z in range(z_max):
    print("%d / %d" %(z, z_max))
    for y in range(y_max):
        #line = np.zeros(shape=(x_max,), dtype=np.int8)
        line = lil_matrix(shape=(1, x_max), dtype=np.int8)

        for action in actions:

            y_rng = y >= action[3] and y <= action[4]
            z_rng = z >= action[5] and z <= action[6]

            if y_rng and z_rng:
                line[action[1] : action[2] + 1] = action[0]                               
        
        sum += line[line > 0].shape[0]

print(sum)
interact(local=locals())
