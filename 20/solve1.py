#!/usr/bin/python3

import numpy as np
from itertools import product
from code import interact

rounds = 2

def get_input():
    global rounds
    file_name = "input"
    #file_name = "test_data"
    
    with open(file_name, "r") as in_file:
        key = in_file.readline().strip()
        key = key.replace(".", "0")
        key = key.replace("#", "1")
        key = list(key)
        key = np.asarray(key, dtype=np.int8)
    
        in_file.readline()
    
        image = list()
        for line in in_file:
            line = line.strip()
            line = line.replace(".", "0")
            line = line.replace("#", "1")
            line = list(line)
            image.append(line)
    
        image = np.asarray(image, dtype=np.int8) 
    
        padding = 2 * (rounds + 1)
        tmp = np.zeros(shape=(image.shape[0] + 2 * padding, image.shape[1] + 2 * padding), dtype=np.int8)
        tmp[padding : -padding, padding : -padding] += image 
        image = tmp
    
        return image, key
    
def to_int(vec):

    res = 0
    for idx in range(vec.shape[0]):
        res += vec[vec.shape[0] - 1 - idx] * 2**idx
    return res

def print_img(img):
    for idx in range(img.shape[0]):
        for jdx in range(img.shape[1]):
            if img[idx, jdx] == 0:
                print('.', end='')
            else:
                print('#', end='')
        print()


in_img, key = get_input()
out_img = np.zeros(shape=in_img.shape, dtype=np.int8)

for _ in range(rounds):

    out_img[out_img ==1] -= 1

    for idx, jdx in product(range(1, in_img.shape[0] - 1), range(1, in_img.shape[1] - 1)):
        vec = in_img[idx-1 : idx+2, jdx-1 : jdx+2].flatten()
        out_img[idx, jdx] = key[to_int(vec)]

    in_img = out_img.copy() 
    in_img = in_img[1:-2, 1:-2]
    print_img(out_img)
    print()

print(out_img[out_img > 0].shape)
interact(local=locals())
