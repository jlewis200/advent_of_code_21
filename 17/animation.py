#!/usr/bin/python3

import numpy as np
from code import interact
import pyglet
from pyglet import shapes
from time import sleep

W = 1920
H = 880
W = int(0.95 * W)
H = int(0.95 * H)


file_name = "input"
#file_name = "test_data"

def simulate(v_x, v_y, x_1, y_1, x_2, y_2):
    x_rng = range(x_1, x_2 + 1)
    y_rng = range(y_1, y_2 + 1)

    res = False
    y_max = -9999
    x = 0
    y = 0

    while x <= x_2 and y >= y_1:
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
 
try:
    tuples = np.load("tuples.npy", allow_pickle=True)

except IOError:
   
        tuples = list()
        max_max = -9999
        v__x = 0
        v__y = 0
        for v_x in range(0, 160):
            for v_y in range(-110, 200): 
                max_ = simulate(v_x, v_y, x_1, y_1, x_2, y_2)
                if max_ > -9999:
                    tuples.append((v_x, v_y))
    
                if max_ > max_max:
                    v__x = v_x
                    v__y = v_y
                    max_max = max_
                print(*(max_max, v__x, v__y), sep=' ')
        
        tuples.sort()
        tuples = np.asarray(tuples, dtype=np.float64)
        np.save("tuples.npy", tuples, allow_pickle=True)

np.random.seed(0)
np.random.shuffle(tuples)

class Transformer:
    def __init__(self, W, H):
        self.left_pad = 0.3
        self.right_pad = 0.3
        self.total_width = self.left_pad + 1 + self.right_pad
        self.x_scale = W / self.total_width
        
        self.top_pad = 4
        self.bottom_pad = 1
        self.total_height = self.top_pad + 1 + self.bottom_pad
        self.y_scale = H / self.total_height

    def transform(self, x, y):
        x = self.x_scale * (self.left_pad + x)
        y = self.y_scale * (self.bottom_pad + y)
        return x, y

class Probe:
    def __init__(self, v_x, v_y, x_scaler, y_scaler, step_size, rectangle):
        self.x = 0
        self.y = 0
        self.v_x = v_x
        self.v_y = v_y
        self.x_scaler = x_scaler
        self.y_scaler = y_scaler
        self.step_size = step_size
        self.step_count = 0
        self.rectangle = rectangle


    def step(self):
        self.x += self.v_x / self.step_size
        self.y += self.v_y / self.step_size
        self.step_count += 1

        if self.step_count >= self.step_size:
            self.step_count = 0
            self.update_velocity()


    def update_velocity(self):
        self.v_x -= np.clip(self.v_x, -1/self.x_scaler, 1/self.x_scaler)
        self.v_y -= 1 / self.y_scaler


    
transformer = Transformer(W, H)

#scale tuples by x_2, y_1
tuples[:, 0] /= x_2
tuples[:, 1] /= abs(y_2)

window = pyglet.window.Window(W, H, style='borderless')
@window.event
def on_draw():
    window.clear()
    batch.draw()

batch = pyglet.graphics.Batch()

target  = shapes.Rectangle(*transformer.transform(x_1, y_1), *transformer.transform(x_2 - x_1, y_2 - y_1), color=(0, 255, 0), batch=batch)

probes = list()
tuples = tuples.tolist()

def update(dt):
    global probes
    global batch
    global target
    
    if len(probes) < 100:
        color=(255, 0, 0)
        coord = tuples.pop()
        rectangle = shapes.Rectangle(*transformer.transform(*coord), 20, 20, color=color, batch=batch)
        probe = Probe(*coord, x_2, abs(y_2), 60, rectangle)
        probes.append(probe)

    removes = list()
    for probe in probes:
        probe.step()
        x, y = transformer.transform(probe.x, probe.y)
        probe.rectangle.x = x
        probe.rectangle.y = y

        if probe.x > transformer.total_width or probe.y < -2:
            removes.append(probe)

    for probe in removes:
        probes.remove(probe)

    

if __name__ == "__main__":
#    for idx in range(10, -1, -1):
#        print(idx)
#        sleep(1)

    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()


interact(local=locals())
