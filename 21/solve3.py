#!/usr/bin/python3

import numpy as np
from itertools import product
from scipy.special import binom

from code import interact
GRAPH_NODES = (3, 7)

def get_input():
    global rounds
    file_name = "input"
    #file_name = "test_data"
    
    with open(file_name, "r") as in_file:
        p1 = int(in_file.readline().split(":")[1].strip())
        p2 = int(in_file.readline().split(":")[1].strip())
   
        return p1 , p2

def wrap(pos):
    while pos > 10:
        pos -= 10
    return pos

def print_dict(d):
    keys = list(d.keys())
    keys.sort()

    sum = 0
    for key in keys:
        print("%d  %d" % (key, d[key]))
        sum += d[key]
    print("sum:  %d" % sum)

#get_combinations()

class Node:

    count = 0

    def __init__(self, roll, freq, p_init, s_init):
        Node.count += 1
        self.id = str(Node.count)
        self.freq = freq
        self.roll = roll 
        self.pos = wrap(p_init + roll)
        self.children = set()
        self.score = 0

        if roll != 0:
            self.score += s_init + self.pos 


        if self.score < 21:
            self.children.add(Node(3, 1, self.pos, self.score))
            self.children.add(Node(4, 3, self.pos, self.score))
            self.children.add(Node(5, 6, self.pos, self.score))
            self.children.add(Node(6, 7, self.pos, self.score))
            self.children.add(Node(7, 6, self.pos, self.score))
            self.children.add(Node(8, 3, self.pos, self.score))
            self.children.add(Node(9, 1, self.pos, self.score))

        self.label = "roll:%d, pos:%d, score:%d" % (self.roll, self.pos, self.score)

    def get_max_depth(self, depth=0):
        depth += 1

        if len(self.children) > 0:
            return max([child.get_max_depth(depth) for child in self.children])

        else:
            return depth

    def get_node_count(self, count=0):
        return 1 + sum([child.get_node_count(count) for child in self.children])

    def get_node_list(self, node_list=None, depth=0):
        if node_list is None:
            node_list = list()

        if depth > 20:
            return 

        node_list.append(self)

        for child in self.children:
            if child.roll in GRAPH_NODES:
                child.get_node_list(node_list, depth + 1)
            else:
                node_list.append(child)

        return node_list

    def get_edge_list(self, edge_list=None, depth=0):
        if edge_list is None:
            edge_list = list()

        if depth > 20:
            return edge_list

        for child in self.children:
            edge_list.append((self.id, child.id))
            if child.roll in GRAPH_NODES:
                child.get_edge_list(edge_list, depth + 1)

        return edge_list

    def get_ttw_freq(self):
        """
        Get time-to-win frequencies.
        Returns a dict with the number of universes the player terminates for a given number of rolls.

        roll 3,  p1 terminates 100 universes
        roll 4,  p1 terminates 1000 universes
        etc...
        """

        freq_dict = {idx : 0 for idx in range(1, 12)}
        self.ttw_freq(freq_dict, 1, 0)

        return freq_dict

    def ttw_freq(self, freq_dict, freq, rolls):

        #if children exist, this node/roll does not terminate any universes
        if len(self.children) > 0:
            for child in self.children:
                child.ttw_freq(freq_dict, freq * self.freq, rolls + 1)

        #if no children exist, this node/roll does terminate universes
        else:
            #number of universes terminated given by self frequency * incoming frequency
            val = freq * self.freq
            
            try:
                freq_dict[rolls] += val

            except KeyError:
                freq_dict[rolls] = val


p1, p2 = get_input()

p1_tree = Node(0, 1, p1, 0)
p1_freq = p1_tree.get_ttw_freq()

p2_tree = Node(0, 1, p2, 0)
p2_freq = p2_tree.get_ttw_freq()

print("p1:  %d" % p1)
print_dict(p1_freq)
print()

print("p2:  %d" % p2)
print_dict(p2_freq)
print()

p1_win = 0
p2_win = 0
p1_comb = 1
p2_comb = 1

for idx in range(1, 12):
    print("#" * 80)
    print("step:  %d" % idx)
    print()

    #p1
    p1_win_ = p1_freq[idx] * p2_comb
    p1_win += p1_win_
    p1_comb *= 27   
    print("p1 induced universes:  %d" % p1_comb)
    print("p1 step wins/universes terminated:  %d" % p1_win_)

    p1_comb -= p1_freq[idx]
    print("p1 residual universes :  %d" % p1_comb)
    print()
   
    #p2
    p2_win_ = p2_freq[idx] * p1_comb
    p2_win += p2_win_
    p2_comb *= 27
    print("p2 induced universes:  %d" % p2_comb)
    print("p2 step wins/universes terminated:  %d" % p2_win_)

    p2_comb -= p2_freq[idx]
    print("p2 residual universes :  %d" % p2_comb)
    print()
    
    print("p1 win total:  %d" % p1_win)
    print("p2 win total:  %d" % p2_win)


    print("#" * 80)
    print()


print(p1_tree.get_max_depth())
print(p1_tree.get_node_count())
print(p2_tree.get_max_depth())
print(p2_tree.get_node_count())

import dash
import math

import dash_cytoscape as cyto
import dash_html_components as html

app = dash.Dash(__name__)
p1_node_list = p1_tree.get_node_list()
p1_edge_list = p1_tree.get_edge_list()

nodes = [{'data': {'id': node.id, 'label': node.label}} for node in p1_node_list]
edges = [{'data': {'source': source, 'target': target}} for source, target in p1_edge_list]

elements = nodes + edges

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-layout-6',
        elements=elements,
        style={'width': '100%', 'height': '1000px'},
        layout={
            'name': 'breadthfirst',
            'roots': '[id = "1"]'
        }
    )
])


#import code
#code.interact(local=locals())

if __name__ == '__main__':
    app.run_server(debug=True)
