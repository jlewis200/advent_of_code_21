#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

class Node:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.comp = False
        self.weight = weight
        self.path = np.inf

def update(data, idx, jdx, idx_, jdx_):
    if idx_ >= 0 and \
       idx_ < data.shape[0] and \
       jdx_ >= 0 and \
       jdx_ < data.shape[1]:

        tent_path = data[idx, jdx].path + data[idx_, jdx_].weight
        if tent_path < data[idx_, jdx_].path:
            data[idx_, jdx_].path = tent_path
 
def sort_f(node):
    return node.path

with open(file_name, "r") as in_file:

    data = list()

    jdx = 0
    for line in in_file:
        numbers = list(line.strip())
        data.append([Node(idx, jdx, int(numbers[idx])) for idx in range(len(numbers))])
        jdx += 1

    data = np.asarray(data)
    path = np.full(shape=data.shape, fill_value=np.inf)
    data[0, 0].path = 0

    nodes = list()
    for idx in range(data.shape[0]):
        for jdx in range(data.shape[1]):
            nodes.append(data[idx, jdx])
    
    while len(nodes) > 0:
        nodes.sort(key=sort_f)
        node = nodes.pop(0)
        idx = node.y
        jdx = node.x

        #update left
        update(data, idx, jdx, idx - 1, jdx)

        #update down
        update(data, idx, jdx, idx, jdx + 1)

        #update right
        update(data, idx, jdx, idx + 1, jdx)

        #update up
        update(data, idx, jdx, idx, jdx - 1)
            

    print(data[-1 ,-1].path)
    interact(local=locals())
