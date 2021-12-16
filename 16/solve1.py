#!/usr/bin/python3

import numpy as np
from code import interact

file_name = "input"
#file_name = "test_data"

class Parser:
    def __init__(self):
        self.version_sum = 0

    def parse(self, data):
        if len(data) < 11:
            return ""

        print(data)
        ver = int(data[:3], base=2)
        self.version_sum += ver

        typ = int(data[3:6], base=2)
        data = data[6:]
    
        if typ == 4:
            data, value = self.parse_literal(data)
            print(value)
    
        else:
            values = list()
            len_typ = data[0]
            data = data[1:]
    
            if len_typ == "0":
                n_bits = int(data[:15], base=2)
                print("n_bits:  %d" % n_bits)
                data = data[15:]
                prev_data_len = len(data)
    
                while (prev_data_len - len(data)) < n_bits:
                    data, value  = self.parse(data)
                    values.append(value)
    
            else:
                n_packets = int(data[:11], base=2)
                print("n_packets:  %d" % n_packets)
                data = data[11:]
    
                for _ in range(n_packets):
                    data, value = self.parse(data)
                    values.append(value)

            #sum
            if typ == 0:
                value = sum(values)

            #product
            if typ == 1:
                value = np.prod(values)

            #minimum
            if typ == 2:
                value = min(values)

            #maximum
            if typ == 3:
                value = max(values)

            #greater than
            if typ == 5:
                value = values[0] > values[1]

            #less than
            if typ == 6:
                value = values[0] < values[1]

            #equality
            if typ == 7:
                value = values[0] == values[1]

        return data, value

    def parse_literal(self, data):
        literal = ""
        idx = 0
        cont = True
    
        while cont:
            cont = data[idx] == "1"
            literal += data[idx + 1 : idx + 5]
            idx += 5
    
        return data[idx:], int(literal, base=2)
    

with open(file_name, "r") as in_file:
    data = in_file.read().strip()
    data = f"{int(data, base=16):0{4*len(data)}b}"
    
    parser = Parser()
    _, value = parser.parse(data)
    print("version sum:  %d" % parser.version_sum)
    print("value:  %d" % value)

