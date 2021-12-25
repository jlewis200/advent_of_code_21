#!/usr/bin/python3

import numpy as np
import pdb
from copy import deepcopy
from code import interact

def get_data():
    file_name = "input2"
#    file_name = "test_data2"
    
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
            self.terminal = None
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
            
            if self.terminal is not None and \
               self.val == self.terminal and \
               self.d.val in [self.terminal, '#']:
                return paths

            Node.root.clear()
            self.visited = True
            self.get_paths(paths, self.val, partial)

        return paths

    def get_paths(self, paths, val, partial):

        #if terminal, and val is correct, and lower val is wall or correct
        if self.terminal is not None and \
           val == self.terminal:

            #traverse to bottom of bucket
            #check if all are either wall or correct
            homogeneous = True
            tmp_node = self.d
            while tmp_node.terminal is not None:
                homogeneous = homogeneous and tmp_node.val in [tmp_node.terminal, '#']
                tmp_node = tmp_node.d

            if homogeneous:

                #print("terminal logic")
                #interact(local=locals())
    #            pdb.set_trace()
                paths.clear()

                paths.append((self, len(partial)))
                return True

        #add if not no-rest, and not visited, and not terminal
        if self.val != '_' and not self.visited and self.terminal is None: 
            paths.append((self, len(partial)))
        
        self.visited = True
        complete = False

        if  not complete and \
            self.l is not None and \
            self.l.val in ['.', '_'] and \
            not self.l.visited:

            tmp_path = partial + "l"
            complete = self.l.get_paths(paths, val, tmp_path)

        if  not complete and \
            self.r is not None and \
            self.r.val in ['.', '_'] and \
            not self.r.visited:

            tmp_path = partial + "r"
            complete = self.r.get_paths(paths, val, tmp_path)

        if  not complete and \
            self.u is not None and \
            self.u.val in ['.', '_'] and \
            not self.u.visited:

            tmp_path = partial + "u"
            complete = self.u.get_paths(paths, val, tmp_path)

        if  not complete and \
            self.d is not None and \
            self.d.val in ['.', '_'] and \
            not self.d.visited:

            tmp_path = partial + "d"
            complete = self.d.get_paths(paths, val, tmp_path)
        
        return complete

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

    def get_terminals(self, terminals=None):

        if terminals is None:
            terminals = dict()

        node = self

        terminal_char = 'A'

        while node is not None:
            if node.val in ['A', 'B', 'C', 'D']:
                
                node.terminal = terminal_char

                if terminal_char not in terminals.keys():
                    terminals[terminal_char] = list()

                terminals[terminal_char].append(node)

                terminal_char = chr(ord(terminal_char) + 1)

            node = node.r

        if self.d is not None:
            self.d.get_terminals(terminals)

        return terminals 

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
                node.u.r.d = node.r

            node = node.r

    return root

def is_complete(terminals):
    complete = True

    for char in ['A', 'B', 'C', 'D']:
        for idx in range(4):
            complete = complete and terminals[char][idx].val == char

    return complete

def solve(pieces, terminals, move_counts, energies, energy):
    global min_energy

    if energy >= min_energy:
        return

    if False:
        indent = 0
        for char in ['A', 'B', 'C', 'D']:
            for idx in range(4):
                indent += move_counts[char][idx]
         
        node_str = str(Node.root.d)
        for line in node_str.split('\n'):
             print("    " * indent, end='')
             print(line)
#    print_dict(move_counts)

    if is_complete(terminals):
        if energy < min_energy:
            min_energy = energy
            print("energy:  %d" % energy)
    #        exit()
            #energies.append(energy)
        return

    #for char in ['A', 'B', 'C', 'D']:
    for char in ['D', 'C', 'B', 'A']:
        for idx in range(4):
            if move_counts[char][idx] < 2:
                
                original_position = pieces[char][idx]
                
                dests = pieces[char][idx].get_dests()         
                pieces[char][idx].val = '.'

                if len(dests) > 0:
                    move_counts[char][idx] += 1
                    for dest, cost in dests:

                        if move_counts[char][idx] == 2 and \
                           dest.terminal is None:
                            continue

                        dest.val = char
                        pieces[char][idx] = dest
                        solve(pieces, terminals, deepcopy(move_counts), energies, energy + cost*(10**(ord(char) - 0x41)))
                        dest.val = '.'
                    move_counts[char][idx] -= 1

                pieces[char][idx] = original_position
                pieces[char][idx].val = char

board = get_data()
root = setup_nodes(board)

min_energy = 47330
pieces = root.get_pieces()
terminals = root.get_terminals()
print_dict(pieces)
print_dict(terminals)

move_counts = dict()
move_counts['A'] = [0, 0, 0, 0]
move_counts['B'] = [0, 0, 0, 0]
move_counts['C'] = [0, 0, 0, 0]
move_counts['D'] = [0, 0, 0, 0]

#############
#.C_C_B_._..#
###B#.#.#D###
###D#.#B#A###
###D#B#A#C###
###A#D#C#A###
#############


#pieces['C'][0].val = '.'
#pieces['C'][0] = root.d.d.r.r
#pieces['C'][0].val = 'C'
#
#pieces['C'][1].val = '.'
#pieces['C'][1] = root.d.d.r.r.r.r
#pieces['C'][1].val = 'C'
#
#pieces['B'][1].val = '.'
#pieces['B'][1] = root.d.d.r.r.r.r.r.r
#pieces['B'][1].val = 'B'
#node = pieces['B'][1]

energies = list()
print(root)

interact(local=locals())
solve(pieces, terminals, move_counts, energies, 0)
print(energies)
#print(min(energies))
#interact(local=locals())
