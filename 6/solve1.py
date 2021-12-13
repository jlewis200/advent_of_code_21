#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

with open(file_name, "r") as in_file:
    data = np.asarray(in_file.read().strip().split(','), np.int64)
    population = np.zeros(shape=(9,))

    frequencies = dict()
    for val in range(9):
        population[val] = data[data == val].shape[0]

    interact(local=locals())
    for idx in range(256):
        new_fish = population[0]

        for jdx in range(8):
            population[jdx] = population[jdx + 1]

        population[6] += new_fish
        population[8] = new_fish

        print(population[:9])
    print(population.sum())
