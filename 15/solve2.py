#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
file_name = "test_data"

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
        tmp = [Node(idx, jdx, int(numbers[idx])) for idx in range(len(numbers))]
        tmp2 = tmp.copy()
        for idx in range(1, 5):
            for node in tmp2:
                tmp += [Node(node.x + (idx * len(tmp2)), node.y, max(1, (node.weight + idx) % 10))]
        data.append(tmp)
        jdx += 1

    tmp = data.copy()
    for idx in range(1, 5):
        for line in tmp:
            tmp2 = [Node(node.x, node.y + (idx * len(tmp)), max(1, (node.weight + idx) % 10)) for node in line]
            data.append(tmp2)

    data = np.asarray(data)
    interact(local=locals())
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
