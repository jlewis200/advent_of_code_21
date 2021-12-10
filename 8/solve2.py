#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

score = 0


with open(file_name, "rt") as in_file:
    data = in_file.read().split("\n")

    sum = 0
    for line in data:
        print(line)

        try:
            signal, output = line.split("|")
        except:
            break

        signal = [set(sig) for sig in signal.split()]
        output = [set(out) for out in output.split()]

        d_map = {idx : set("z") for idx in range(10)}
        for sig in signal:
            sig_len = len(sig)

            #1
            if sig_len == 2:
                d_map[1] = sig
                #print(d_map)

            #4
            elif sig_len == 4:
                d_map[4] = sig
                #print(d_map)

            #7
            elif sig_len == 3:
                d_map[7] = sig
                #print(d_map)
            
            #8
            elif sig_len == 7:
                d_map[8] = sig
                #print(d_map)

        for sig in signal:
            sig_len = len(sig)
            
            #0 6 9
            if sig_len == 6:
#                interact(local = locals())         
                if sig & d_map[7] != d_map[7]:
                    d_map[6] = sig
                    #print(d_map)

                elif sig & d_map[4] == d_map[4]:
                    d_map[9] = sig
                    #print(d_map)

                else:
                    d_map[0] = sig
                    #print(d_map)


        for sig in signal:
            sig_len = len(sig)
            
            #2 3 5
            if sig_len == 5:
                if sig & d_map[7] == d_map[7]:
                    d_map[3] = sig
                    #print(d_map)

                elif sig & d_map[6] == sig:
                    d_map[5] = sig
                    #print(d_map)

                else:
                    d_map[2] = sig
                    #print(d_map)

#        interact(local=locals())
        out_val = ""
        for out in output:
            for key in d_map.keys():
                if out == d_map[key]:
                    out_val += str(key)
        print(out_val)
        sum += int(out_val)




#    interact(local=locals())
    print(sum)
