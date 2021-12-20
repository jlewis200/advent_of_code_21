#!/usr/bin/python3

import numpy as np
from math import floor, ceil
from code import interact

file_name = "input"
file_name = "test_data"
#file_name = "test_data2"


def find_delim(line, idx):

    while idx < len(line) and line[idx] != ']' and line[idx] != ',':
        idx += 1

    return idx


class Number:

    idx = 0

    def __init__(self, line, idx=0, parent=None):
        self.left = None
        self.right = None
        self.value = None
        self.depth = 0
        self.parent = parent

        if idx < len(line):
            if line[idx] == '[':
                self.left = Number(line, idx + 1, self)
                self.right = Number(line, Number.idx, self)
    
            else:
                Number.idx = find_delim(line, idx)
                self.value = int(line[idx:Number.idx])
    
            Number.idx += 1

    def print(self):
        if self.value is None:
            print('[', end='')
            self.left.print()
            print(',', end='')
            self.right.print()
            print(']', end='')

        else:
            print(self.value, end='')

    def to_list(self, ret_list=None):
        if ret_list is None:
            ret_list = list()

        if self.value is not None:
            ret_list.append(self)
            print(self.value)

        if self.left is not None:
            self.left.to_list(ret_list)

        if self.right is not None:
            self.right.to_list(ret_list)

        return ret_list

    def update_depth(self, depth=0):

        self.depth = depth

        if self.left is not None:
            self.left.update_depth(depth + 1)

        if self.right is not None:
            self.right.update_depth(depth + 1)


def print_line(line):
    depth = 0
    for char in line:
        if char == '[':
            depth += 1
            print()
            print(depth, end=' ')
        elif char == ']':
            depth -= 1
            print()
            print(depth, end=' ')
        elif char == ',':
            print(',', end='')
        else:
            print(char, end='')

def explode(nlist, idx):
    if idx > 0:
        nlist[idx - 1].value += nlist[idx].value
        if nlist[idx - 1] >= 10:
            split(nlist, idx - 1)

    if idx < len(nlist) - 1:
        nlist[idx + 1].value += nlist[idx].value
        if nlist[idx + 1] >= 10:
            split(nlist, idx + 1)


with open(file_name, "rt") as in_file:
    
    numbers = list()
    for line in in_file:
        Number.idx = 0
        numbers.append(Number(line))
        print_line(line)

    n1 = numbers.pop(0)
    n2 = numbers.pop(0)
    tmp = Number("")
    tmp.left = n1
    tmp.right = n2
    n1 = tmp
    
    nlist = n1.to_list()
    nlist.update_depth()

    for idx in range(len(nlist)):
        if nlist[idx].depth == 4:
            explode(nlist, idx)

        if nlist[idx].value >= 10:
            nlist[idx]
    print()
    interact(local=locals())
