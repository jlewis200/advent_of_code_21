#!/usr/bin/python3

import numpy as np
import pyglet
from pyglet import shapes
from time import sleep
from code import interact

file_name = "input"; board_max = 2881; steps_per_frame = 100; max_intensity = 2499
#file_name = "test_data"; board_max = 315; steps_per_frame = 1; max_intensity = 2499

def update_(weight, path, complete, prev, idx, jdx, idx_, jdx_):
    res = False

    if idx_ >= 0 and \
       idx_ < weight.shape[0] and \
       jdx_ >= 0 and \
       jdx_ < weight.shape[1] and \
       not complete[idx_, jdx_]:

        tent_path = path[idx, jdx] + weight[idx_, jdx_]
        if tent_path < path[idx_, jdx_]:
            path[idx_, jdx_] = tent_path
            prev[idx_, jdx_] = (idx, jdx)
            res = True

    return res
 
def sort_f(node):
    return node[0]

W = 1920
H = 1080
W = int(0.95 * W)
H = int(0.95 * H)


weight = None
with open(file_name, "r") as in_file:
    weight = list()
    jdx = 0
    for line in in_file:
        weight.append(list(line.strip()))
        jdx += 1


weight = np.asarray(weight, dtype=np.int64)
tile_shape = weight.shape
weight = np.tile(weight, (5, 5))

#increment tiles along x axis
for idx in range(1, 5):
    weight[idx * tile_shape[0]:, 0:] += 1

#increment tiles along y axis
for idx in range(1, 5):
    weight[0:, idx * tile_shape[1]:] += 1

#wrap around if greater than 9
weight[weight > 9] -= 9

complete = np.full(shape=weight.shape, fill_value=False)
prev = np.zeros(shape=(weight.shape[0], weight.shape[1], 2), dtype=np.int64)
path = np.full(shape=weight.shape, fill_value=board_max + 1)
path[0, 0] = 0

nodes = [(path[0, 0], (0, 0))] 

w = W//weight.shape[0]
h = H//weight.shape[1]
d = min(w, h)
W = d * weight.shape[0]
H = d * weight.shape[1]

p_max = path.max()

window = pyglet.window.Window(W, H, style = 'borderless')
@window.event
def on_draw():
    window.clear()
    batch.draw()


batch = pyglet.graphics.Batch()
rectangles = np.full(shape=weight.shape, fill_value=None)

for idx in range(rectangles.shape[0]):
    for jdx in range(rectangles.shape[1]):
        r = 0
        g = 0 
        b = 0
        rectangles[idx, jdx] = shapes.Rectangle(idx * d, jdx * d, d, d, color=(r, g, b), batch=batch)

def sigmoid(X):
   return 1 - np.exp(-X / 0.2)

intensity = np.zeros(shape=weight.shape, dtype=np.int64)
complete_once = False
prev_shortest_path = list()
def update(dt):
    global complete
    global nodes
    global weight
    global path
    global prev
    global complete_once
    global prev_shortest_path 
    global steps_per_frame
    global intensity

    coords_ = []
    coord = (-1, -1)
#    print(len(nodes))
    for _ in range(steps_per_frame):
        if len(nodes) > 0:
            print(intensity.max())
            nodes.sort(key=sort_f)
            coord = nodes.pop(0)[1]
        
            coords_ = [(coord[0] - 1, coord[1]), 
                       (coord[0] + 1, coord[1]), 
                       (coord[0], coord[1] - 1), 
                       (coord[0], coord[1] + 1)]
        
            for coord_ in coords_: 
                if update_(weight, path, complete, prev, *coord, *coord_):
                    nodes.append((path[coord_], coord_))
            
            complete[coord] = True
    

    for coord_ in prev_shortest_path:
        coord_ = (coord_[0] % path.shape[0], coord_[1] % path.shape[1])

        if path[coord_] > board_max:
            r = 0
            g = 0
            b = 0
        
        else:
            g = int(255 * (sigmoid(intensity[coord_] / max_intensity)))#int((path[coord_] * 255) // p_max)
            r = g//2
            b = g
       
        rectangles[coord_].color = (r, g, b)

    if not complete[-1, -1]:
        shortest_path = [(coord)]
        while coord != (0, 0):
            coord = tuple(prev[coord])
            shortest_path.insert(0, coord)
    
        for coord in shortest_path:
            r = 255
            g = 255 
            b = 255
            rectangles[coord].color = (r, g, b)
            intensity[coord] += 1
        prev_shortest_path = shortest_path


if __name__ == "__main__":
    for idx in range(10, -1, -1):
        print(idx)
        sleep(1)

    pyglet.clock.schedule_interval(update, 10**-10)
    pyglet.app.run()
