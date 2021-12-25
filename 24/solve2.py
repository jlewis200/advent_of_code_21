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

stages = list()

for op in ops:
    
    if op[0] == "inp":
        stages.append(list())
        stages[-1].append(["inp", "z"])

    stages[-1].append(op)

#generate all possible output values for each stage except the last
#we're only interested in an output of 0 from the last stage, so no need to 
#generate all last stage outputs
out_zs_list = []
in_zs = {0}

for idx, stage in enumerate(stages[:-1]):
    print("stage:  %d" % idx)
    print("    w,  inz, outz")

    try:
        out_zs_list.append(np.load("out_zs_array_%d.npy" % idx, allow_pickle=True))
        out_zs = set(out_zs_list[-1].tolist())
        print("loaded")

    except IOError:
        
        out_zs = set() #out z for this stage, in z for next stage
        
        for w in range(1, 10):
            for z in in_zs:

                regs = interpret(stage, [z, w])

    #            if regs['z'] not in out_zs:
    #                print("%10d,%10d,%10d" % (w, z, regs['z']))
                out_zs.add(regs['z'])
        
        out_zs_list.append(np.asarray(list(out_zs), dtype=np.int64))
        np.save("out_zs_array_%d.npy" % idx, out_zs_list[-1], allow_pickle=True)
        print("generated")
 
    print("out_zs len:  %d" % len(out_zs))
    print("out_zs min:  %d" % min(out_zs))
    print("out_zs max:  %d" % max(out_zs))
    print()

    in_zs = out_zs

interact(local=locals())

out_zs_list.insert(0, {0})
out_zs = {0}

for idx in range(len(stages) - 1, -1, -1):
    print("stage:  %d" % idx)
    print("    w,    z")

    stage = stages[idx]
    in_zs = set()

    for w in range(1, 10):
        for z in out_zs_list[idx]:

            regs = interpret(stage, [z, w])
            if regs['z'] in out_zs:
                print("%10d,%10d,%10d" % (w, z, regs['z']))
                in_zs.add(z)
 
    print("in_zs len:  %d" % len(out_zs))
    print("in_zs min:  %d" % min(out_zs))
    print("in_zs max:  %d" % max(out_zs))
    print()

    out_zs = in_zs

interact(local=locals())
