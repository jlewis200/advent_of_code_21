#!/usr/bin/python3

import numpy as np
from code import interact

def get_ops():
    file_name = "input"
#    file_name = "digit0"

    with open(file_name, "r") as in_file:
        ops = list()

        for line in in_file:
            ops.append(line.strip().split())

    return ops

def print_dict(d):

    keys = list(d.keys())
    keys.sort()

    for key in keys:
        print("%s : " % key, end='')
        print(d[key])
    print()

def interpret(ops, data):

    reg_set = {'w', 'x', 'y', 'z'}
    regs = {reg : 0 for reg in reg_set}

    for op in ops:
        
        #destination register
        dst = op[1] 

        #source from register or literal
        src = None

        if len(op) == 3:
            src = regs[op[2]] if op[2] in reg_set else int(op[2])
        
        if op[0] == "inp":
            regs[dst] = data.pop(0)

        elif op[0] == "add":
            regs[dst] += src

        elif op[0] == "mul":
            regs[dst] *= src          

        elif op[0] == "div":
            regs[dst] //= src

        elif op[0] == "mod":
            regs[dst] %= src

        elif op[0] == "eql":
            regs[dst] = 1 if regs[dst] == src else 0

        else:
            print("syntax error")
            return
    
    return regs

ops = get_ops()

n = 12345678912345
n = 92967699949891
n = 91411143612181
data = [int(e) for e in list(str(n))]

regs = interpret(ops, data)
print(regs['z'])

interact(local=locals())
