#!/usr/bin/python3

import numpy as np
from code import interact

def get_ops(filename):
    """
    Get the operations from a program.

    Return a list of operations.  Each operation is a list of len 2 or 3:
                  0,       1,                 2                 
        instruction, dst reg, [src reg/literal]
    """

    with open(filename, "r") as in_file:
        ops = list()

        for line in in_file:
            ops.append(line.strip().split())

    return ops

def print_dict(d):
    """
    Print a dict by the sorted value of it's keys.
    """

    keys = list(d.keys())
    keys.sort()

    for key in keys:
        print("%s : " % key, end='')
        print(d[key])
    print()

def interpret(ops, data):
    """
    Interpret a program defined by a list of ops using input data.
    """

    #set of registers
    reg_set = {'w', 'x', 'y', 'z'}

    #define a dict of registers and set to 0
    regs = {reg : 0 for reg in reg_set}

    #for each operation
    for op in ops:
        
        #destination register
        dst = op[1] 

        #source from register or literal
        src = None

        #get src register or literal if length of operation is 3
        if len(op) == 3:
            src = regs[op[2]] if op[2] in reg_set else int(op[2])
       
        #evaluate the operation
        if op[0] == "inp":
            regs[dst] = data.pop(0)

        elif op[0] == "add":
            regs[dst] += src

        elif op[0] == "mul":
            regs[dst] *= src          

        elif op[0] == "div":
            regs[dst] //= src #integer division

        elif op[0] == "mod":
            regs[dst] %= src

        elif op[0] == "eql":
            regs[dst] = 1 if regs[dst] == src else 0

        else:
            print("syntax error")
            return
    
    return regs

def solve(filename="input"):
    """
    The main solving logic.

    The validation program is broken into 14 stages where an input digit is
    combined with the z register in various ways.  The z register retains the 
    result of the stage and is carried forward to the next stage.  All other 
    registers are cleared before use, so the output of each stage is dependent 
    only on the input digit and the value of the incoming z register.  At stage
    0, the z register is 0.  

    The possible inputs of each stage are the possible input digits [1, 9] and
    the possible outputs of the previous stage.  For stage 0 the possible 
    incoming z values is only {0}.  

    The z outputs of stage 0 are calculated.  The possible input values for 
    stage 1 are all combinations of the input digit and the outputs of stage 0.

    The outputs of all stages are generated in order and saved to numpy arrays.

    Once the possible outputs of each stage are generated, the inputs which 
    produce valid MONAD digits are enumerated in reverse.  The stage 13 z output 
    of the program when provided a valid model number is 0.  All combinations of
    z outputs from stage 12 are combined with each input digit [1, 9] and run
    through stage 13.  Any inputs which do not produce the correct z output of 0
    are eliminated.  This process continues in reverse:

        non-validated input zs for stage[i] are combined with input digits [1, 9]
        any non-validated input z which results in a validated z input to stage i+1 is added to a validated input list 
    producing input/z cominations as 

    """

    ops = get_ops(filename)
    stages = list()

    #break the validation program into one stage per input digit
    #insert an "inp z" instruction ahead of each stage of the validation program
    #this instrumentation allows consideration of a single stage in isolation
    for op in ops:
        if op[0] == "inp":
            stages.append(list())
            stages[-1].append(["inp", "z"])

        stages[-1].append(op)

    stages_poss_out = get_stages_poss_out(stages)
    stages_valid_tuples = get_stages_valid_tuples(stages, stages_poss_out)

    numbers = get_numbers(stages_valid_tuples, 0, 0, "")                
    valid_number_count = sum([validate(ops, number) for number in numbers])
    
    print("total number count:  %d" % len(numbers))
    print("valid number count:  %d" % valid_number_count)
    print("max model number:  %d" % max(numbers))
    print("min model number:  %d" % min(numbers))

def get_stages_poss_out(stages):
    """
    Forward enumeration phase.

    Returns the possible z outputs for each stage.
    """

    print("forward enumeration phase")

    #generate all possible output values for each stage except the last
    #we're only interested in an output of 0 from the last stage

    stages_poss_out = [] #list of possible outputs for each stage
    poss_in = {0} #set of possible inputs for the current stage

    for idx, stage in enumerate(stages[:-1]):
        print("stage:  %d" % idx)

        try:
            #attempt to load the stage outputs from disk
            stages_poss_out.append(np.load("poss_out_array_%d.npy" % idx, allow_pickle=True))
            poss_out = set(stages_poss_out[-1].tolist())
            print("loaded")

        except IOError:
            #if loading from disk fails, generate the possible stage outputs
            poss_out = set() #out z for this stage, in z for next stage
            
            for w in range(1, 10):
                for z in poss_in:
                    regs = interpret(stage, [z, w])
                    poss_out.add(regs['z'])
            
            stages_poss_out.append(np.asarray(list(poss_out), dtype=np.int64))
            np.save("poss_out_array_%d.npy" % idx, stages_poss_out[-1], allow_pickle=True)
            print("generated")
     
        print("poss_out len:  %d" % len(poss_out))
        print("poss_out min:  %d" % min(poss_out))
        print("poss_out max:  %d" % max(poss_out))
        print()

        poss_in = poss_out
    
    return stages_poss_out

def get_stages_valid_tuples(stages, stages_poss_out):
    """
    Backwards elimination phase.

    Eliminate all inputs which do not produce a valid output.

    Returns a by-stage list of valid (in_z, out_z, in_w) tuples.
    """

    print("backwards elimination phase")

    #list contining the valid z_in, z_out, and inputs for each stage
    stages_valid_tuples = list()

    #insert possible output for stage[-1], which is input for stage[0]
    stages_poss_out.insert(0, {0}) 

    #the only valid output for stage 13 is 0
    valid_out = {0}

    for idx in range(len(stages) - 1, -1, -1):
        print("stage:  %d" % idx)
        print("      z_in     z_out      w_in")

        #insert a new valid tuples list for the current stage
        #iteration of the stages is in reverse, so the list is also built in reverse
        #entries are (z_in, z_out, w_in)
        stages_valid_tuples.insert(0, list())

        stage = stages[idx]
        valid_in = set()

        for w in range(1, 10):
            for z in stages_poss_out[idx]:
                regs = interpret(stage, [z, w])

                if regs['z'] in valid_out:
                    print("%10d,%10d,%10d" % (z, regs['z'], w))
                    stages_valid_tuples[0].append((z, regs['z'], w))
                    valid_in.add(z)
    
        print("valid_in len:  %d" % len(valid_out))
        print("valid_in min:  %d" % min(valid_out))
        print("valid_in max:  %d" % max(valid_out))
        print()

        #the valid inputs for the current stage[i] will be the valid outputs for stage[i-1]
        valid_out = valid_in
    
    return stages_valid_tuples

def get_numbers(svts, idx, z_in, partial):
    """
    Recursively build the numbers.  Append to the list once the terminal tuple
    is reached.
    """

    numbers = list()
    
    if idx == len(svts):
        numbers.append(int(partial))
    
    else:
        for vt in svts[idx]:
            if vt[0] == z_in:
                numbers += get_numbers(svts, idx + 1, vt[1], partial + str(vt[2]))
    
    return numbers

def validate(ops, model_number):
    """
    Validate a model number using the provided operations.
    """
    
    #form a list of single digit integers
    data = [int(e) for e in list(str(model_number))]

    #run the validation program against the model number
    regs = interpret(ops, data)

    #return true if the z register is 0
    return regs['z'] == 0

if __name__ == "__main__":
    solve("input")
