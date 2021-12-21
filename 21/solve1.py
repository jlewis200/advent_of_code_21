#!/usr/bin/python3

import numpy as np
from itertools import product
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

p1, p2 = get_input()

rolls = list(range(1, 101))
rolls *= 10

p1_score = 0
p2_score = 0
n_rolls = 0
res = 0

while len(rolls) > 0:
    
    n_rolls += 3
    p1 += rolls.pop(0) + rolls.pop(0) + rolls.pop(0)
    p1 = wrap(p1)
    p1_score += p1
    if p1_score >= 1000:
        res = n_rolls * p2_score
        break

    n_rolls += 3
    p2 += rolls.pop(0) + rolls.pop(0) + rolls.pop(0)
    p2 = wrap(p2)
    p2_score += p2
    if p2_score >= 1000:
        res = n_rolls * p1_score
        break

print(res)
interact(local=locals())
