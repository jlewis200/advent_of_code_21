#!/usr/bin/python3

import numpy as np
from code import interact

MAX_ITR = 1000

def get_data(filename):
    """
    Get grid layout from file.

    Returns a numpy ndarray with the following character mapping:
        '.' -> 0
        '>' -> 1
        'v' -> 2
    """

    lines = list()

    with open(filename, "r") as in_file:

        for line in in_file:
            #map characters to (character) numbers
            line = line.replace(".", "0")
            line = line.replace(">", "1")
            line = line.replace("v", "2")

            #split rows into a list single characters, append to lines
            lines.append(list(line.strip()))

    #return the list of lists as a 2-d ndarray
    return np.asarray(lines, dtype=np.int8)

def print_grid(grid):
    """
    Print a grid, substituting the numerical values in the ndarray with their
    character equivalents.
    """

    char_map = dict()
    char_map[0] = "."
    char_map[1] = ">"
    char_map[2] = "v"

    for idx in range(grid.shape[0]):

        for jdx in range(grid.shape[1]):

            print(char_map[grid[idx, jdx]], end='')

        print()

    print()

def solve(filename="input", debug=False):
    """
    The main solving logic.
    """

    grid = get_data(filename)
    print_grid(grid)

    itr = 1
    modified = True

    while modified and itr < MAX_ITR:
        modified = False
        print("iteration:  %d" % itr)
        
        #east-to-west herd logic 

        #position changes are made to a copy of the grid
        #this simplifies the logic and avoids moveing a cucumber more than once per pass
        tmp = grid.copy()

        #for each row
        for idx in range(grid.shape[0]):
            
            #for each column
            for jdx in range(grid.shape[1]):

                #calc the possibly wrapped position to the right of [idx, jdx]
                jdx_ = (jdx + 1) % grid.shape[1]
    
                #if position holds a E-W element and right position is open
                if grid[idx, jdx] == 1 and grid[idx, jdx_] == 0:

                    #move element right
                    tmp[idx, jdx] = 0
                    tmp[idx, jdx_] = 1
                    modified = True
       
        if debug:
            print_grid(tmp)

        #north-to-south herd logic 
        
        #copy updated temp grid to "grid"
        grid = tmp.copy()

        #for each row
        for idx in range(grid.shape[0]):    

            #for each column
            for jdx in range(grid.shape[1]):
           
                #calc possibly wrapped lower index
                idx_ = (idx + 1) % grid.shape[0]

                #if position holds a N-S element and lower position is open
                if grid[idx, jdx] == 2 and grid[idx_, jdx] == 0:

                    #move element down
                    tmp[idx, jdx] = 0
                    tmp[idx_, jdx] = 2
                    modified = True

        if debug:
            print_grid(tmp)

        #update grid and iteration counter
        grid = tmp
        itr += 1

    #print final grid layout 
    print_grid(grid)

if __name__ == "__main__":
    #solve("test_data", True)
    solve("input", False)
