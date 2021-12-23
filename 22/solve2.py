#!/usr/bin/python3

import numpy as np
from scipy.sparse import lil_matrix, csc_matrix, csr_matrix
from code import interact

def get_data():
    file_name = "input"
#    file_name = "test_data2"
    
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



def do_action(action, intervals):
    x0 = action[1]
    x1 = action[2]
    
    #print("action: %d %d %d" % tuple(action))
    #off
    if action[0] == 0:
        
        intervals_len = len(intervals)
        idx = 0
        while idx < intervals_len:

            #range of interval
            int_rng = range(intervals[idx][0], intervals[idx][1] + 1)
 
            #complete overlap, eliminate
            if intervals[idx][0] in range(x0, x1 + 1) and intervals[idx][1] in range(x0, x1 + 1):
                #print("off, case 0")
                intervals.pop(idx)
                idx -= 1
                intervals_len -= 1
           
            #no overlap, do nothing
            elif x0 not in int_rng and x1 not in int_rng:
                #print("off, case 1")
                pass
            
            #partial central overlap, split
            elif x0 in int_rng and x1 in int_rng:
                #print("off, case 2")
                right = intervals[idx][1]
                intervals[idx][1] = x0 - 1
                intervals.insert(idx + 1, [x1 + 1, right])
                idx += 1
                intervals_len += 1

            #partial right overlap, update right side of interval
            elif x0 in int_rng:
                #print("off, case 3")
                intervals[idx][1] = x0 - 1

            #partial left overlap, update left side of interval 
            elif x1 in int_rng:
                #print("off, case 4")
                intervals[idx][0] = x1 + 1
            
            idx += 1

        intervals_len = len(intervals)
        idx = 0
        while idx < intervals_len:

            if intervals[idx][0] > intervals[idx][1]:
                intervals.pop(idx)
                idx -= 1
                intervals_len -= 1
            
            idx += 1

    #on
    if action[0] == 1:

        updated = False

        intervals_len = len(intervals)
        idx = 0
        while idx < intervals_len:

            #range of interval
            int_rng = range(intervals[idx][0], intervals[idx][1] + 1)
            
            #no overlap, do nothing
            if x0 not in int_rng and x1 not in int_rng:
                #print("on, case 0")
                pass

            #complete overlap, update left and right
            elif intervals[idx][0] in range(x0, x1 + 1) and intervals[idx][1] in range(x0, x1 + 1):
                #print("on, case 1")
                intervals[idx][0] = x0
                intervals[idx][1] = x1
                updated = True

            #partial central overlap, do nothing
            elif x0 in int_rng and x1 in int_rng:
                #print("on, case 2")
                updated = True

            #partial right overlap, update right side of interval
            elif x0 in int_rng:
                #print("on, case 3")
                intervals[idx][1] = x1
                updated = True

            #partial left overlap, update left side of interval 
            elif x1 in int_rng:
                #print("on, case 4")
                intervals[idx][0] = x0
                updated = True

            idx += 1

        if not updated:
            #print("on, case 5")
            inserted = False

            for idx in range(len(intervals)):
                if x0 < intervals[idx][0]: 
                    intervals.insert(idx, [x0, x1])
                    inserted = True
                    break

            if not inserted:
                intervals.append([x0, x1])

        intervals_len = len(intervals)
        idx = 0
        while idx < intervals_len - 1:

            if intervals[idx][1] + 1 >= intervals[idx + 1][0]:
                #print("merging")
                #print(intervals)
                intervals[idx][1] = intervals[idx + 1][1]
                intervals.pop(idx + 1)
                idx -= 1
                intervals_len -= 1

            idx += 1

def sum_intervals(intervals):

    sum = 0
    
    for interval in intervals:
        sum += interval[1] - interval[0] + 1

    if len(intervals) > 0 and sum < 1:
        #print("sum error")
        #print(intervals)
        exit()
    return sum

intervals = []
a = list()

#a.append((1, 5, 14))
#a.append((1, 5, 14))
#a.append((1, 6, 13))
#a.append((1, 3, 5))
#a.append((1, 3, 6))
#a.append((1, 2, 4))
#a.append((1, 14, 15))
#a.append((1, 16, 17))
#a.append((1, 15, 16))
#a.append((0, 7, 9))
#a.append((0, 2, 2))
#a.append((0, 2, 4))
#a.append((0, 2, 6))
#a.append((0, 17, 17))
#a.append((0, 11, 12))
#a.append((0, 15, 18))

a.append((1, 5, 14))
a.append((1, 2, 3))
a.append((1, 4, 4))
a.append((0, 4, 4))
a.append((0, 3, 5))
a.append((0, 1, 7))
a.append((1, 2, 2))
a.append((0, 0, 17))


#for action in a:
#    do_action(action, intervals)
#    #print(intervals)
#    #print(sum_intervals(intervals))
#
#exit(0)
#interact(local=locals())
actions = get_data()

x_max = actions[:, 1:3].max() + 1
y_max = actions[:, 3:5].max() + 1
z_max = actions[:, 5:7].max() + 1

sum = 0

for z in range(z_max + 1):
    print("%d / %d" %(z, z_max))
    for y in range(y_max + 1):
        #line = np.zeros(shape=(x_max,), dtype=np.int8)
        #line = lil_matrix(shape=(1, x_max), dtype=np.int8)

        intervals = []

        for action in actions:

            y_rng = y >= action[3] and y <= action[4]
            z_rng = z >= action[5] and z <= action[6]

            if y_rng and z_rng:
                #line[action[1] : action[2] + 1] = action[0]                               
                do_action(action[:3], intervals)

        line_sum = sum_intervals(intervals)
        ##print("%d %d " %(y, z) + str(intervals) + " %d" % )        
        #print("%d %d %d" % (y, z, line_sum))        
        #sum += line[line > 0].shape[0]
        sum += line_sum 

print(sum)
#interact(local=locals())
