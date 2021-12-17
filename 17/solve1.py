#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
file_name = "test_data"

def simulate(v_x, v_y, x_1, y_1, x_2, y_2):
    x_rng = range(x_1, x_2 + 1)
    y_rng = range(y_1, y_2 + 1)

    res = False
    y_max = -9999
    x = 0
    y = 0

    while x <= x_2 and y >= y_2:
#        print(*(x, y, v_x, v_y, res), sep=' ')
        x += v_x
        y += v_y

        v_x -= np.clip(v_x, -1, 1)
        v_y -= 1

        if x in x_rng and y in y_rng:
            res = True

        if y > y_max:
            y_max = y

    if not res:
        y_max = -9999

    return y_max

with open(file_name, "r") as in_file:
    data = in_file.read().strip()
    x_1, x_2 = data.split()[-2].split('=')[-1].split("..")
    y_1, y_2 = data.split()[-1].split('=')[-1].split("..")

    x_1 = int(x_1)
    x_2 = int(x_2[:-1])
    y_1 = int(y_1)
    y_2 = int(y_2)

    results = list()
    max_max = -9999
    v__x = 0
    v__y = 0
    for v_x in range(0, 40):
        for v_y in range(-80, 200): 
            max_ = simulate(v_x, v_y, x_1, y_1, x_2, y_2)
            if max_ > -9999:
                results.append(max_)

            if max_ > max_max:
                v__x = v_x
                v__y = v_y
                max_max = max_
            print(*(max_max, v__x, v__y), sep=' ')
    
    results.sort()
    print(results[-1])
    print(len(results))
    interact(local=locals())
