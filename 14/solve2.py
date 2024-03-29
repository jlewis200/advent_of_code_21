#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

with open(file_name, "r") as in_file:
    sp = list(in_file.readline().strip())
    in_file.readline()
    res = list()
    char_freq = dict()
    pair_freq = dict()

    pirs = dict()
    for line in in_file:
        pir = line.strip().split(" -> ")
        pirs[pir[0]] = pir[1]

    for idx in range(len(sp) - 1):
        pair = sp[idx] + sp[idx + 1]

        try:
            pair_freq[pair] += 1
        except:
            pair_freq[pair] = 1

        try:
            char_freq[sp[idx]] += 1
        except:
            char_freq[sp[idx]] = 1
    try:
        char_freq[sp[-1]] += 1
    except:
        char_freq[sp[-1]] = 1


    for _ in range(40):
        
        tmp_pair_freq = dict()
        for pair in pair_freq.keys():

            occurrences = pair_freq[pair]
            new_char = pirs[pair]

            print("pair:  %s, char:  %s, occurrences:  %d" % (pair, new_char, occurrences))

            try:
                tmp_pair_freq[pair[0] + new_char] += occurrences
            except:
                tmp_pair_freq[pair[0] + new_char] = occurrences

            try:
                tmp_pair_freq[new_char + pair[1]] += occurrences
            except:
                tmp_pair_freq[new_char + pair[1]] = occurrences

            try:
                char_freq[new_char] += occurrences
            except:
                char_freq[new_char] = occurrences

        pair_freq = tmp_pair_freq


                
    freq = list(char_freq.values())
    freq.sort(reverse=True)

    print(pair_freq)
    print(char_freq)
    print(freq)
    print(freq[0] - freq[-1])
    interact(local=locals())
