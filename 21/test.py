#!/usr/bin/python3

from itertools import product

freq = dict()

class N:
    def __init__(self):
        self.n = 0

n = N()

def calc(n, pos, score, depth, roll):
    pos += roll

    while pos > 10:
        pos -= 10
  
    if depth % 3 == 0:
        score += pos

    if depth >= 9:
        if score >= 21:
            n.n += 1
        return

    else:
        calc(n, pos, score, depth + 1, 1)
        calc(n, pos, score, depth + 1, 2)
        calc(n, pos, score, depth + 1, 3)

init = 10

for init in range(1, 11):
    n.n = 0
    calc(n, init, 0, 1, 1)
    calc(n, init, 0, 1, 2)
    calc(n, init, 0, 1, 3)
    print(n.n)   
    
    
    win = 0
    loss = 0
    
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                for d in range(1, 4):
                    for e in range(1, 4):
                        for f in range(1, 4):
                            for g in range(1, 4):
                                for h in range(1, 4):
                                    for i in range(1, 4):
               
                                        pos = init
                                        score = 0
                            
                                        pos += a + b + c
                            
                                        if pos > 10:
                                            pos -= 10
                            
                                        score += pos
                            
                                        pos += d + e + f
                            
                                        if pos > 10:
                                            pos -= 10
                            
                                        score += pos
                            
                                        pos += g + h + i 
                            
                                        if pos > 10:
                                            pos -= 10
                            
                                        score += pos
                            
                                        if score >= 21:
                                            win += 1
                                        else:
                                            loss += 1
    
    
    print(win)
    print(win+loss)
from code import interact
interact(local=locals())
