#!/usr/bin/python3

import numpy as np
from math import floor, ceil
from code import interact

file_name = "input"
file_name = "test_data"
file_name = "test_data2"


def find_delim(line, idx):

    while idx < len(line) and line[idx] != ']' and line[idx] != ',':
        idx += 1

    return idx


class Number:

    idx = 0
    prev = None
    forward = None

    def __init__(self, line, idx=0, parent=None, depth=0):
        self.parent = parent
        self.left = None
        self.right = None
        self.value = None

        if line[idx] == '[':
            self.left = Number(line, idx + 1, parent=self, depth=depth + 1)
            self.right = Number(line, Number.idx, parent=self, depth=depth + 1)

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

    def explode_left(self, value):
#        if self.parent is not None and \
#           self.parent.left is not None and \
#           self.parent.left.value is not None:
#            self.parent.left.value += value
#
#        elif self.parent is not None:
#            self.parent.explode_left(value)

        if len(path) > 1:
            path[-2].value += value
        
    def explode_right(self, value):
        if self.left is not None and \
           self.left.value is not None:
            self.parent.right.value += value

        elif self.parent is not None:
            self.parent.explode_right(value)

    def split():
        self.left = Number("%d" % floor(self.value / 2))
        self.right = Number("%d" % ceil(self.value / 2))
        self.value = None

    def reduce(self, depth):
        """
        prev := previous node with non-None value
        forward := value to pass forward to the next non-None value
        """

        if Number.forward is not None and \
           self.value is not None:
            self.value += Number.forward
            Number.forward = None
            #return?

        if depth == 4 and \
           self.left is not None and \
           self.right is not None and \
           self.left.value is not None and \
           self.right.value is not None:

            if Number.prev is not None:
               Number.prev.value += self.left.value

            Number.forward = self.right.value

            self.left = None
            self.right = None
            self.value = 0
            #return here?

        if self.value is not None:
            Number.prev = self


        if self.value is not None and \
           self.value >= 10:
            self.split()
            #return here?

        if self.left is not None:
            self.left.reduce(depth + 1)

        if self.right is not None:
            self.right.reduce(depth + 1)


            

with open(file_name, "rt") as in_file:
    
    numbers = list()
    for line in in_file:
        n_numbers = line.count(',') + 1
        numbers.append(Number(line))

    for number in numbers:
        number.print() 
        print(" "*8, end='')
        Number.prev = None
        Number.forward = None
        number.reduce(0)
        number.print()
        print()


    print()
    print()
    interact(local=locals())
