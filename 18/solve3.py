#!/usr/bin/python3

import numpy as np
from math import floor, ceil
from code import interact

file_name = "input"
#file_name = "test_data2"


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
        self.left = None
        self.right = None
        self.value = None

        if idx < len(line):
            if line[idx] == '[':
                self.left = Number(line, idx + 1)
                self.right = Number(line, Number.idx)
    
            else:
                Number.idx = find_delim(line, idx)
                self.value = int(line[idx:Number.idx])
    
            Number.idx += 1

    def to_list(self, ret_list=None):
        if ret_list is None:
            ret_list = list()

        ret_list.append(self)

        if self.left is not None:
            self.left.to_list(ret_list)

        if self.right is not None:
            self.right.to_list(ret_list)

        return ret_list


    def print(self):
        char_array = np.full(shape=(5, 180), fill_value=' ')

        idx = 0
        jdx = -1

        for c in self.to_str():
            if c == '[':
                jdx += 1
            char_array[jdx, idx] = c
            if c == ']':
                jdx -= 1

            idx += 1

        for jdx in range(5):
            for idx in range(180):
                print(char_array[jdx, idx], end='')
            print()

            

    def to_str(self):
        res = ""

        if self.value is None:
            res += '['
            res += self.left.to_str()
            res += ','
            res += self.right.to_str()
            res += ']'

        else:
            res += str(self.value)

        return res 

    def split(self):
                
        if self.value is not None and \
           self.value >= 10 and \
           not Number.modified:
            self.left = Number("%d" % floor(self.value / 2))
            self.right = Number("%d" % ceil(self.value / 2))
            self.value = None
            Number.modified = True
            return

        else:
            if self.left is not None:
                self.left.split()

            if self.right is not None:
                self.right.split()
            
    def explode(self, depth):
        """
        prev_node := previous node with non-None value
        fwd_value := value to pass forward to the next non-None value
        """

        if Number.fwd_value is not None and \
           self.value is not None:
            self.value += Number.fwd_value
            Number.fwd_value = None
            return

        #explode criteria
        if depth == 4 and \
           self.left is not None and \
           self.right is not None and \
           self.left.value is not None and \
           self.right.value is not None and \
           not Number.modified:

            Number.modified = True
            
            #explode leftward
            if Number.prev_node is not None:
                Number.prev_node.value += self.left.value

            #set forward value for rightward explosion
            Number.fwd_value = self.right.value

            self.left = None
            self.right = None
            self.value = 0

        #set previous number for possible future use in leftward explosion
        if self.value is not None:
            Number.prev_node = self

        if self.left is not None:
            self.left.explode(depth + 1)

        if self.right is not None:
            self.right.explode(depth + 1)

    def reduce(self):
        Number.modified = True

        while Number.modified:
            Number.modified = False
            Number.prev_node = None
            Number.fwd_value = None

            self.explode(0)
            
#            print(100*'=')
#            self.print()
#            print()
            
            if Number.modified:
                continue
            self.split()
#            print(100*'=')
#            print("split")
#            self.print()
#            print()

    def get_magnitude(self):
        res = 0
        if self.value is not None:
            res = self.value

        else:
            res += 3 * self.left.get_magnitude()
            res += 2 * self.right.get_magnitude()

        return res

with open(file_name, "rt") as in_file:

    largest = 0
    
    numbers = list()
    for line in in_file:
        line = line.strip()
        n_numbers = line.count(',') + 1
        numbers.append(Number(line))

#    #reduce all prior to addition
#    for number in numbers:
#        number.reduce()


    #add numbers
    n1 = numbers.pop(0)

    while len(numbers) > 0:
        n2 = numbers.pop(0)

        tmp = Number("")
        tmp.left = n1
        tmp.right = n2
        n1 = tmp

        n1.reduce()
    print(n1.get_magnitude())
    print(largest)
    print()
    #interact(local=locals())
