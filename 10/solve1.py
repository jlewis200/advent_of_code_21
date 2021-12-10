#!/usr/bin/python3

import numpy as np
from code import interact

scores = {}
scores[')'] = 3
scores[']'] = 57
scores['}'] = 1197
scores['>'] = 25137

ochars = ['(', '[', '{', '<']
cchars = [')', ']', '}', '>']

c_pairs = {}
c_pairs['('] = ')'
c_pairs['['] = ']'
c_pairs['{'] = '}'
c_pairs['<'] = '>'

file_name = "input"
#file_name = "test_data"

with open(file_name, "rt") as in_file:
    data = in_file.read().split()

    score = 0
    for line in data:
        stack = list()

        for char in line:
#            print("%d %s" % (len(stack), str(stack))) 
            if char in ochars:
                stack.append(char)

            elif char in cchars and len(stack) == 0:
                print("incomplete")

            elif char in cchars:
                closer = stack.pop()

#                interact(local=locals())
                if c_pairs[closer] != char:
                    score += scores[char]
#                    print(scores[char])
                    break

            else:
                print("non-standard char")
print(score)
