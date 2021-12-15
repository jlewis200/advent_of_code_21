#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

class Node:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
        self.path = np.inf

def update(data, idx, jdx, idx_, jdx_):
    res = False

    if idx_ >= 0 and \
       idx_ < data.shape[0] and \
       jdx_ >= 0 and \
       jdx_ < data.shape[1]:

        tent_path = data[idx, jdx].path + data[idx_, jdx_].weight
        if tent_path < data[idx_, jdx_].path:
            data[idx_, jdx_].path = tent_path
            res = True

    return res

 
def sort_f(node):
    return node.path

def get_val(val):
    if val < 10:
        return val
    else:
        return (val % 10) + 1


with open(file_name, "r") as in_file:

    data = list()

    jdx = 0
    for line in in_file:
        numbers = list(line.strip())
        tmp = [Node(idx, jdx, int(numbers[idx])) for idx in range(len(numbers))]
        tmp2 = tmp.copy()
        for idx in range(1, 5):
            for node in tmp2:
                tmp += [Node(node.x + (idx * len(tmp2)), node.y, get_val(node.weight + idx))]
        data.append(tmp)
        jdx += 1

    tmp = data.copy()
    for idx in range(1, 5):
        for line in tmp:
            tmp2 = [Node(node.x, node.y + (idx * len(tmp)), get_val(node.weight + idx)) for node in line]
            data.append(tmp2)

    data = np.asarray(data)
    data[0, 0].path = 0

    nodes = [data[0, 0]]
    
    nodes.sort(key=sort_f)
    while len(nodes) > 0:
        print("remaining: %d" % len(nodes))
        nodes.sort(key=sort_f)
        node = nodes.pop(0)
        idx = node.y
        jdx = node.x

        #update left
        if update(data, idx, jdx, idx - 1, jdx):
            nodes.append(data[idx - 1, jdx])

        #update down
        if update(data, idx, jdx, idx, jdx + 1):
            nodes.append(data[idx, jdx + 1])


        #update right
        if update(data, idx, jdx, idx + 1, jdx):
            nodes.append(data[idx + 1, jdx])

        #update up
        if update(data, idx, jdx, idx, jdx - 1):
            nodes.append(data[idx, jdx - 1])

    print(data[-1 ,-1].path)
