#!/usr/bin/python3

import numpy as np
from code import interact

def get_data():
    file_name = "input"
    file_name = "test_data"
    
    with open(file_name, "r") as in_file:
        board = list()
   
        line_len = 0

        for line in in_file:
            line = line[:-1]
            line = line.replace(' ', '#')

            if len(line) > line_len:
                line_len = len(line)
            
            line += '#' * (line_len - len(line))

            board.append(list(line))

        board = np.asarray(board)
        return board

def print_dict(d):

    keys = list(d.keys())
    keys.sort()

    for key in keys:
        print("%s : " % key, end='')
        print(d[key])
    print()

def get_moves(board, pieces, label):
    location = pieces[label]

class Node:

    root = None
    
    def __init__(self, val=None, rest=True):
            self.val = val
            self.visited = False
            self.l = None
            self.r = None
            self.u = None
            self.d = None

            if not rest and self.val == '.':
                self.val = '_'

            if val == "root":
                Node.root = self

    def __str__(self):
        res = ""

        node = self

        while node is not None:
            res += node.val
            node = node.r

        res += '\n'
        
        if self.d is not None:
            res += str(self.d)

        return res

    def clear(self):
        
        node = self

        while node is not None:
            node.visited = False
            node = node.r

        if self.d is not None:
            self.d.clear()

    def get_dests(self, paths=None, partial=None):

        if paths is None:
            paths = list()

        if partial is None:
            partial = ""

        if self.val in ['A', 'B', 'C', 'D']:
            Node.root.clear()
            self.get_paths(paths, partial)

        return paths

    def get_paths(self, paths, partial):
        self.visited = True

        if self.val != '_' and len(partial) > 0: #maybe remove len check to automatically consider doing nothing?  Probably not...
            paths.append(partial)

        if  self.l is not None and \
            self.l.val in ['.', '_'] and \
            not self.l.visited:

            tmp_path = partial + "l"
            self.l.get_paths(paths, tmp_path)

        if  self.r is not None and \
            self.r.val in ['.', '_'] and \
            not self.r.visited:

            tmp_path = partial + "r"
            self.r.get_paths(paths, tmp_path)

        if  self.u is not None and \
            self.u.val in ['.', '_'] and \
            not self.u.visited:

            tmp_path = partial + "u"
            self.u.get_paths(paths, tmp_path)

        if  self.d is not None and \
            self.d.val in ['.', '_'] and \
            not self.d.visited:

            tmp_path = partial + "d"
            self.d.get_paths(paths, tmp_path)

    def get_pieces(self, pieces=None):

        if pieces is None:
            pieces = dict()

        node = self

        while node is not None:
            if node.val in ['A', 'B', 'C', 'D']:
            
                if node.val not in pieces.keys():
                    pieces[node.val] = list()

                pieces[node.val].append(node)

            node = node.r

        if self.d is not None:
            self.d.get_pieces(pieces)

        return pieces 

def setup_nodes(board):
    root = Node("root")
    row = root

    for idx in range(board.shape[0]):
        
        row.d = Node(board[idx, 0])
        row.d.u = row
        row = row.d
        node = row 

        for jdx in range(1, board.shape[1]):
           
            rest = jdx not in [3, 5, 7, 9]
            node.r = Node(board[idx, jdx], rest=rest)
            node.r.l = node

            if node.u is not None and node.u.r is not None:
                node.r.u = node.u.r
                node.u.r.d = node.d

            node = node.r

    return root

board = get_data()

min_energy = 999999999
pieces = root.get_pieces()
print_dict(pieces)

move_counts = dict()
move_counts['A'] = [0, 0]
move_counts['B'] = [0, 0]
move_counts['C'] = [0, 0]
move_counts['D'] = [0, 0]

def solve(root, min_energy):

    for char in ['A', 'B', 'C', 'D']:
        for idx in range(2):
            if move_counts[char][idx] < 2:
                    
                energy = 0

                root = setup_nodes(board)
                dests = pieces[p1][p1_idx].get_dests()




                


#print(board)
#print()
#print(root)

interact(local=locals())
