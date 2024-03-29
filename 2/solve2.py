#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

with open(file_name, "r") as in_file:

    data = list()
    for line in in_file:
        data.append(line.split())
    
    x_pos = 0
    y_pos = 0
    aim = 0
    for move in data:
        if move[0] == "forward":
            x_pos += int(move[1])
            y_pos += aim * int(move[1])

        elif move[0] == "down":
            aim += int(move[1])

        elif move[0] == "up":
            aim -= int(move[1])

    print(x_pos * y_pos)

    interact(local=locals())
    
    
