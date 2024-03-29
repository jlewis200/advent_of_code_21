#!/usr/bin/python3

import numpy as np
from ast import literal_eval as make_tuple
from code import interact

file_name = "input"
#file_name = "test_data"

with open(file_name, "r") as in_file:
    
    lines = in_file.read().strip().split()
    lines = [list(line) for line in lines]
    data = np.asarray(lines, np.int64)
    
    tmp = data
    idx = 0
    while tmp.shape[0] > 1:
        gamma = int(tmp[:, idx].mean() * 2)
        tmp = tmp[tmp[:, idx] == gamma]
        idx += 1
    
    val1 = 0
    for pow, digit in enumerate(tmp[0][::-1]):
        val1 += digit * 2**pow
    print(val1)    

    tmp = data
    idx = 0
    while tmp.shape[0] > 1:
        gamma = 1 - int(tmp[:, idx].mean() * 2)
        tmp = tmp[tmp[:, idx] == gamma]
        idx += 1

    val2 = 0
    for pow, digit in enumerate(tmp[0][::-1]):
        val2 += digit * 2**pow
    print(val2)    


    print(val1 * val2)    
    interact(local=locals())
    
    
