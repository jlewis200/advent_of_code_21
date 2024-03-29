#!/usr/bin/python3

import numpy as np
from ast import literal_eval as make_tuple
from code import interact

file_name = "input"
#file_name = "test_data"

def check_board(bb):   
    """
    bb is a numpy array with shape (5, 5)
    """

    res = False

    for idx  in range(5):
        #sum along row 'idx'
        if bb[idx, :].sum() == 5:
            res = True

        #sum along column 'idx'
        elif bb[:, idx].sum() == 5:
            res = True
        
    return res

def board_val(b, bb):
    return b[bb != True].sum()

with open(file_name, "r") as in_file:
    draws = in_file.readline().strip().split(',')
    draws = np.asarray(draws, dtype=np.int64)

    in_file.readline()
    lines = in_file.read().split('\n')[:-1]

    boards = list()
    idx = 0
    while idx < len(lines):
        board = list()

        for jdx in range(idx, idx + 5):
            board.append(lines[jdx].strip().split())

        idx += 6
        boards.append(board)

    boards = np.asarray(boards, dtype=np.int64)
    boards_bool = np.full(shape=boards.shape, fill_value=False)
   
    wins = 0
    winset = set()
    for draw in draws:
        for jdx in range(len(boards)):
            b = boards[jdx]
            bb = boards_bool[jdx]

            bb += b == draw

            if check_board(bb):
                wins += 1
                winset.add(jdx)
            if len(winset) == boards.shape[0]:
                print(board_val(b, bb) * draw)
                print(board_val(b, bb))
                print(draw)
                print(jdx)
                print(winset)
                print()
                break 


    print(winset)
    interact(local=locals())
    
    
