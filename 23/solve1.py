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
    
        return actions

class Cube:
    
    cubes = list()

    def __init__(on, x0, x1, y0, y1, z0, z1):
        self.x0 = x0
        self.x1 = x1 + 1
        self.y0 = y0
        self.y1 = y1 + 1
        self.z0 = z0
        self.z1 = z1 + 1

        self.xrng = range(self.x0, self.x1)
        self.yrng = range(self.y0, self.y1)
        self.zrng = range(self.z0, self.z1)
        
        self.volume = (x1 - x0) * (y1 - y0) * (z1 - z0)

        for cube in Cube.cubes:
            overlap_coords = self.find_overlap(cube)


        Cube.cubes.append(self)


def xfrm_coord(x0, x1, y0, y1, z0, z1):
    x0 += 50
    y0 += 50
    z0 += 50
    x1 += 51
    y1 += 51
    z1 += 51

    return x0, x1, y0, y1, z0, z1

actions = get_data()
grid = np.full(shape=(101, 101, 101), fill_value=False)
for action in actions:
    if action[0] == 0:
        coord = xfrm_coord(*action[1:])
        grid[coord[0]:coord[1], coord[2]:coord[3], coord[4]:coord[5]] = False

    elif action[0] == 1:
        coord = xfrm_coord(*action[1:])
        grid[coord[0]:coord[1], coord[2]:coord[3], coord[4]:coord[5]] = True

    print(grid[grid == True].shape)
interact(local=locals())
