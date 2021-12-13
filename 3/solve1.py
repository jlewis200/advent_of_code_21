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
    
    gamma = ""

    for idx in range(data.shape[1]):
        gamma += str(int(data[:, idx].mean() * 2))

    epsilon = ""

    for char in gamma:
        if char == "0":
            epsilon += "1"
        else:
            epsilon += "0"

    print(gamma)
    print(epsilon)

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    print(gamma * epsilon)
    interact(local=locals())
    
    
