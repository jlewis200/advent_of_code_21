#!/usr/bin/python3

from multiprocessing import Pool

def f(x):
    return x*x

with Pool(8) as pool:
    print(pool.map(f, range(4)))
