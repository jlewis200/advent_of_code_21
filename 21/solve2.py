#!/usr/bin/python3

import numpy as np
from itertools import product
from scipy.special import binom

from code import interact

def get_input():
    global rounds
    file_name = "input"
    #file_name = "test_data"
    
    with open(file_name, "r") as in_file:
        p1 = int(in_file.readline().split(":")[1].strip())
        p2 = int(in_file.readline().split(":")[1].strip())
   
        return p1 , p2

def wrap(pos):
    while pos > 10:
        pos -= 10
    return pos

def get_combinations():
    """ 
    Sum frequencies of rolling 3 3-sided dice
    3  1
    4  3
    5  6
    6  7
    7  6
    8  3
    9  1
    """
    frequencies = dict()

    for idx in range(1, 4):
        for jdx in range(1, 4):
            for kdx in range(1, 4):

                key = idx + jdx + kdx

                try:
                    frequencies[key] += 1

                except KeyError:
                    frequencies[key] = 1

    print_dict(frequencies)

def print_dict(d):
    keys = list(d.keys())
    keys.sort()

    sum = 0
    for key in keys:
        print("%d  %d" % (key, d[key]))
        sum += d[key]
    print("sum:  %d" % sum)

#get_combinations()

class Node:

    count = 0

    def __init__(self, roll, freq, p_init, s_init):
        Node.count += 1
        self.freq = freq
        self.roll = roll 
        self.pos = wrap(p_init + roll)
        self.children = set()
        self.score = 0

        if roll != 0:
            self.score += s_init + self.pos 


        if self.score < 21:
            self.children.add(Node(3, 1, self.pos, self.score))
            self.children.add(Node(4, 3, self.pos, self.score))
            self.children.add(Node(5, 6, self.pos, self.score))
            self.children.add(Node(6, 7, self.pos, self.score))
            self.children.add(Node(7, 6, self.pos, self.score))
            self.children.add(Node(8, 3, self.pos, self.score))
            self.children.add(Node(9, 1, self.pos, self.score))

    def get_ttw_freq(self):
        
        freq_dict = dict()
        self.ttw_freq(freq_dict, 1, 0)

        return freq_dict

    def ttw_freq(self, freq_dict, freq, rolls):

        if len(self.children) > 0:
            for child in self.children:
                child.ttw_freq(freq_dict, freq * self.freq, rolls + 1)

        else:
            try:
                freq_dict[rolls] += freq * self.freq

            except KeyError:
                freq_dict[rolls] = freq * self.freq


p1, p2 = get_input()

p1_tree = Node(0, 1, p1, 0)
p1_freq = p1_tree.get_ttw_freq()

p2_tree = Node(0, 1, p2, 0)
p2_freq = p2_tree.get_ttw_freq()

print("p1:  %d" % p1)
print_dict(p1_freq)
print()

print("p2:  %d" % p2)
print_dict(p2_freq)
print()


p1_freq[1] = 0
p1_freq[2] = 0
p2_freq[1] = 0
p2_freq[2] = 0

for key in p1_freq.keys():
    if key not in p2_freq.keys():
        p2_freq[key] = 0

for key in p2_freq.keys():
    if key not in p1_freq.keys():
        p1_freq[key] = 0


p1_win = 0
p2_win = 0
p1_comb = 1
p2_comb = 1

for idx in range(1, 11):
    print(p1_comb)
    print(p2_comb)

    p1_tmp = p1_freq[idx] * (p2_comb)
    p1_win += p1_tmp
    p1_comb *= 27   
    p1_comb -= p1_freq[idx]

    
    p2_tmp = p2_freq[idx] * (p1_comb)
    p2_win += p2_tmp
    p2_comb *= 27
    p2_comb -= p2_freq[idx]
    
    print("p1: %d" % p1_win)
    print("p2: %d" % p2_win)


print()
total_universes = 444356092776315 + 341960390180808
print("tu: %d" % total_universes)
interact(local=locals())
