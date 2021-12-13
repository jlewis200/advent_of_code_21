#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

X_RNG = range(10)
Y_RNG = range(10)

class Board:
    def __init__(self, data):
        self.data = data
        self.flash_tracker = np.zeros(shape=data.shape)
        self.flash_count = 0

    def check(self, idx, jdx):
        if idx in X_RNG and jdx in Y_RNG and self.data[idx, jdx] > 9:
            self.flash(idx, jdx)
    
    def flash(self, idx, jdx):
        if idx in X_RNG and jdx in Y_RNG and self.flash_tracker[idx, jdx] == 0:
            self.flash_count += 1
            self.data[idx, jdx] = 0
            self.flash_tracker[idx, jdx] = 1

            self.increment(idx - 1, jdx + 0)
            self.increment(idx - 1, jdx + 1)
            self.increment(idx + 0, jdx + 1)
            self.increment(idx + 1, jdx + 1)
            self.increment(idx + 1, jdx + 0)
            self.increment(idx + 1, jdx - 1)
            self.increment(idx + 0, jdx - 1)
            self.increment(idx - 1, jdx - 1)

    def increment(self, idx, jdx):
        if idx in X_RNG and jdx in Y_RNG and self.flash_tracker[idx, jdx] == 0:
            self.data[idx, jdx] += 1
            self.check(idx, jdx)

    def increment_all(self):
        self.data += 1
        self.flash_tracker[:, :] = 0

    def check_all_flash(self):
        if self.flash_tracker.sum() == self.flash_tracker.shape[0] * self.flash_tracker.shape[1]:
            return True
        else:
            return False
        

with open(file_name, "r") as in_file:
    lines = in_file.read().strip().split()
    lines = [list(line) for line in lines]
    data = np.asarray(lines, np.int64)

    board = Board(data)
    for kdx in range(1, 1000):
        board.increment_all()

        for idx in range(data.shape[0]):
            for jdx in range(data.shape[1]):
                board.check(idx, jdx)
                
#        print(board.flash_count) 
        print("%d %d" % (kdx, board.flash_tracker.sum()))
        if board.check_all_flash():
            break
    
