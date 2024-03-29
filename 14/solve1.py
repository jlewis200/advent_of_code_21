#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

with open(file_name, "r") as in_file:
    sp = list(in_file.readline().strip())
    in_file.readline()

    pirs = dict()
    for line in in_file:
        pir = line.strip().split(" -> ")
        pirs[pir[0]] = pir[1]

    for jdx in range(10):
        tmp_sp = list()
        for idx in range(len(sp) - 1):
            pair = sp[idx] + sp[idx + 1]
            tmp_sp.append(sp[idx])
            tmp_sp.append(pirs[pair])
        tmp_sp.append(sp[-1])
        sp = tmp_sp

    sp = np.asarray(sp)
    unique, counts = np.unique(sp, return_counts=True)
    res = counts[counts.argmax()] - counts[counts.argmin()]

    print(res)
    interact(local=locals())
