#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

with open(file_name, "r") as in_file:
    coords = list()
    folds = list()

    for line in in_file:
        coord = line.strip().split(',')
        if len(coord) > 1:
            coords.append(coord)
        elif "y=" in line:
            fold = int(line.strip().split("=")[-1])
            folds.append(("y", fold))
        elif "x=" in line:
            fold = int(line.strip().split("=")[-1])
            folds.append(("x", fold))

    coords = np.asarray(coords, np.int64)

    x_sz = coords[:, 0].max() + 1
    y_sz = coords[:, 1].max() + 1

    grid = np.zeros(shape=(x_sz, y_sz))

    for coord in coords:
        grid[coord[0], coord[1]] = 1
    
    for fold in folds:
        if fold[0] == "y":
            for x in range(grid.shape[0]):
                y_0 = fold[1]
                y_1 = fold[1]
                while y_0 >= 0 and y_1 < grid.shape[1]:
                    grid[x, y_0] += grid[x, y_1]
                    y_0 -= 1
                    y_1 += 1

            grid = grid[:, :fold[1]]

        elif fold[0] == "x":
            for y in range(grid.shape[1]):
                x_0 = fold[1]
                x_1 = fold[1]
                while x_0 >= 0 and x_1 < grid.shape[0]:
                    grid[x_0, y] += grid[x_1, y]
                    x_0 -= 1
                    x_1 += 1

            grid = grid[:fold[1], :]

    np.set_printoptions(threshold=np.inf)


    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            if grid[x, y] > 0:
                print("#", end='')
            else:
                print(" ", end='')
        print("")

