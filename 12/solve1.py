#!/usr/bin/python3

import numpy as np
from copy import copy
from code import interact

file_name = "input"
file_name = "test_data"

class Node:

    paths = set()

    def __init__(self, label):
        self.label = label
        self.big = label.isupper()
        self.edges = set()

    def add_edge(self, other):
        self.edges.add(other)
        other.edges.add(self)

    def find_paths(self, partial_path):
        print(self.label)
        partial_path.append(self)

        if self.label == "end":
            #verify and commit path here
            partial_path_strs = [node.label for node in partial_path]
            path_str = ",".join(partial_path_strs)
            Node.paths.add(path_str)

        else:
            for edge in self.edges:
                if edge not in partial_path or edge.big:
                    edge.find_paths(copy(partial_path))
                

with open(file_name, "r") as in_file:
    data = list()
    for line in in_file:
        data.append(line.strip().split('-'))

    nodes = dict()
    for line in data:

        try:
            src = nodes[line[0]]

        except KeyError:
            src = Node(line[0])
            nodes[line[0]] = src

        try:
            dst = nodes[line[1]]

        except KeyError:
            dst = Node(line[1])
            nodes[line[1]] = dst

        src.add_edge(dst)

         
    nodes["start"].find_paths(list())
    print(Node.paths) 
    print(len(Node.paths))

    interact(local=locals())   
