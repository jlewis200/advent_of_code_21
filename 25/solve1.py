#!/usr/bin/python3

import numpy as np
from code import interact

def get_data():
    filename = "input"
    filename = "test_data"

    lines = list()

    with open(filename, "t") as in_file:

        for line in in_file:
            line.replace(".", 0)
            line.replace(">", 1)
            line.replace("v", 2)

            lines.append(line.strip())

    return np.asarray(filename, dtype=np.int8)

grid = get_data()

interact(local=locals())
