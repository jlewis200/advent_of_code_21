#!/usr/bin/python3

import numpy as np
from math import floor, ceil
from code import interact

file_name = "input"
file_name = "test_data"


def find_delim(line, idx):

    while idx < len(line) and line[idx] != ']' and line[idx] != ',':
        idx += 1

    return idx


class Number:

    idx = 0
    modified = False
    prev_node = None
    fwd_value = None

    def __init__(self, line, idx=0):
        print(len(line))
        self.left = None
        self.right = None
        self.value = None
        self.depth = 0

        if idx < len(line):
            if line[idx] == '[':
                self.left = Number(line, idx + 1)
                self.right = Number(line, Number.idx)
    
            else:
                Number.idx = find_delim(line, idx)
                print(idx)
                print(Number.idx)
                print()
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

    def set_depth(self, depth):
        self.depth = depth

        if self.left is not None:
            self.left.set_depth(depth + 1)
        
        if self.right is not None:
            self.right.set_depth(depth + 1)

    def scan(self):

        #explode criteria
        if self.depth == 4 and \
           self.left is not None and \
           self.right is not None and \
           self.left.value is not None and \
           self.right.value is not None:
           
            Number.clear()
            Number.root.explode(self, 0)
            
        #split criteria
        elif self.value is not None and \
            self.value >= 10:
            self.split()

        if self.left is not None:
            self.left.scan()

        if self.right is not None:
            self.right.scan()
           
    def explode(self, target):

        if Number.prev is not None and self == target:
            Number.prev.value += target.value

        elif Number.prev is not None and Number.prev == target:
            self.value += target.value
        

            if Number.prev_prev is not None and Number.prev_prev.value >= 10:
                Number.prev_prev.split()

            if self.value >= 10:
                self.split() 
            
            return

        Number.prev_prev = Number.prev
        Number.prev = self
        
        if self.left is not None:
            self.left.explode(target) 

        if self.right is not None:
            self.right.explode(target) 

    def split(self):

        self.left = Number("%d" % floor(self.value / 2), depth=depth + 1)
        self.right = Number("%d" % ceil(self.value / 2), depth=depth + 1)
        self.value = None

        if self.left.depth == 4:
            Number.clear()
            Number.root.explode(self.left, 0)

        if self.right.depth == 4:
            Number.clear()
            Number.root.explode(self.right, 0)

    def reduce(self):
        self.set_depth()
        Number.modified = True

        while Number.modified:
            Number.modified = False
            self.scan()

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

with open(file_name, "rt") as in_file:
    
    numbers = list()
    for line in in_file:
        line = line.strip()
        n_numbers = line.count(',') + 1
        numbers.append(Number(line))
        print_line(line)

    #reduce all prior to addition
    for number in numbers:
        number.print() 
        print(" "*8, end='')
        number.reduce()
        number.print()
        print()

    #add numbers
    n1 = numbers.pop(0)

    while len(numbers) > 0:
        n2 = numbers.pop(0)

        print('*' * 80)
        n1.print()
        print()
        n2.print()
        print()
        print()

        tmp = Number("")
        tmp.left = n1
        tmp.right = n2
        n1 = tmp
        n1.set_depth(0)
        n1.print()
        print()       

        n1.reduce()
        n1.print()
        print()

    print()
    print()
#    interact(local=locals())
