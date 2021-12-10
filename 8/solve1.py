#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

score = 0

seg_map = dict()
segments = set("abcdefg")
for segment in segments:
    seg_map[segment] = segments
interact(local=locals())
with open(file_name, "rt") as in_file:
    data = in_file.read().split("\n")

    for line in data:
#        interact(local=locals())
        print(line)
        try:
            signal, output = line.split("|")
        except:
            break

        signal = [set(sig) for sig in signal.split()]
        output = [set(out) for out in output.split()]

        sig_map = dict()

        for sig in signal:
            sig_len = len(sig)

            #2
            if sig_len == 2:
                
            #4
            elif sig_len == 4:

            #7
            elif sig_len == 3:

            #8
            elif sig_len == 7:



        for out in output:
            out_len = len(out)

            #2
            if out_len == 2:
                score += 1

            #4
            elif out_len == 4:
                score += 1

            #7
            elif out_len == 3:
                score += 1

            #8
            elif out_len == 7:
                score += 1




#    interact(local=locals())
    print(score)
