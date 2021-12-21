#!/usr/bin/python3

import numpy as np
from itertools import product
from code import interact

file_name = "input"
#file_name = "test_data"

class Sensor:

    def __init__(self):
        self.beacons = list()

    def add_beacon(self, line):
        self.beacons.append(line.split(","))

    def convert(self):
        self.beacons = np.asarray(self.beacons, dtype=np.int32)
        self.dist = np.zeros(shape=(self.beacons.shape[0], self.beacons.shape[0]), dtype=np.float64)

        for idx in range(self.beacons.shape[0]):
            for jdx in range(self.beacons.shape[0]):

                if idx == jdx:
                    continue

                self.dist[idx, jdx] = (
                    (self.beacons[idx][0] - self.beacons[jdx][0])**2 + 
                    (self.beacons[idx][1] - self.beacons[jdx][1])**2 + 
                    (self.beacons[idx][2] - self.beacons[jdx][2])**2) ** 0.5


with open(file_name, "r") as in_file:
    
    sensors = list()

    for line in in_file:
        line = line.strip()

        if len(line) < 1:
            continue

        elif "---" in line:
            sensors.append(Sensor())

        else:
            sensors[-1].add_beacon(line)

    for sensor in sensors:
        sensor.convert()

    overlaps = list()

    for idx in range(len(sensors) - 1):
        for jdx in range(idx + 1, len(sensors)):
            #67 indicates overlap:  12*11/2 == 66 + 1 for 0
            tmp = np.intersect1d(sensors[idx].dist, sensors[jdx].dist)
            if tmp.shape[0] == 67:
                overlaps.append((idx, jdx, tmp))
    print(overlaps)

    ident = np.asarray([[ 1,  0,  0], 
                        [ 0,  1,  0], 
                        [ 0,  0,  1]])

    rot_y = np.asarray([[ 0,  0,  1], 
                        [ 0,  1,  0], 
                        [-1,  0,  0]])

    rot_x = np.asarray([[ 1,  0,  0], 
                        [ 0,  0, -1], 
                        [ 0,  1,  0]])

    rot_z = np.asarray([[ 0, -1,  0], 
                        [ 1,  0,  0], 
                        [ 0,  0,  1]])


    ref_y = np.asarray([[ 1,  0,  0], 
                        [ 0, -1,  0], 
                        [ 0,  0,  1]])
    transforms = list()

    for x in range(4):
        for y in range(4):
            for z in range(4):

                transform = ident.copy()

                for _ in range(x):
                    transform = rot_x.dot(transform)
                
                for _ in range(y):
                    transform = rot_y.dot(transform)

                for _ in range(z):
                    transform = rot_z.dot(transform)

                transforms.append(transform.copy())
                
                transform = ref_y.dot(transform)
                transforms.append(transform.copy())

    transforms = np.asarray(transforms)
    transforms = np.unique(transforms, axis=0)
    complete = set()
    complete.add(0)
    scanner_centers = [(0,0,0)]

    while len(complete) < len(sensors):
        for overlap in overlaps:
   
            if overlap[0] in complete and overlap[1] not in complete:
                src = overlap[0]
                dst = overlap[1]

            elif overlap[1] in complete and overlap[0] not in complete:
                src = overlap[1]
                dst = overlap[0]

            else:
                continue


            s1 = sensors[src]
            s2 = sensors[dst]
            print(src)
            print(dst)
            pairs = list()
    
            for idx, jdx in product(range(s1.dist.shape[0]), range(s2.dist.shape[0])):
                tmp = np.intersect1d(s1.dist[idx], s2.dist[jdx])
    #            print("intersection %d %d %d" % (idx, jdx, tmp.shape[0]))
                if tmp.shape[0] == 12:
                    
                    print("=" * 80)
                    print("matches")
    
                    for match in tmp:
                        print(np.nonzero(s1.dist[idx] == match))
                        print(np.nonzero(s2.dist[jdx] == match))
                        print()
                        i1 = np.nonzero(s1.dist[idx] == match)[0][0]
                        i2 = np.nonzero(s2.dist[jdx] == match)[0][0]
                        #pairs contains line-order mapping of beacons from s1 to s2
                        pairs.append((i1, i2))
    
                    break
                    print()
    
            #for each pair
            #calculate s2 center relative to s1
            #if different, transform and try again
    
    
            for transform in transforms:
                tmp = transform.dot(s2.beacons.T).T
                        
                s2_centers = list()
                for iii, yyy in pairs:
                    s2_centers.append(tuple(s1.beacons[iii] - tmp[yyy]))
    
                print(set(s2_centers))
                if len(set(s2_centers)) == 1:

                    scanner_centers.append(s2_centers.pop())
                    s2.beacons = tmp + scanner_centers[-1] 
                    complete.add(dst)
                    break
            print()
            print()
   
        concatenated = np.concatenate([sensors[idx].beacons for idx in range(len(sensors))])
        concat_uniq = np.unique(concatenated, axis=0)
        print(concat_uniq.shape)

    max_dist = 0
    for idx in range(len(sensors) - 1):
        for jdx in range(idx, len(sensors)):
            dist = abs(scanner_centers[idx][0] - scanner_centers[jdx][0]) + \
                   abs(scanner_centers[idx][1] - scanner_centers[jdx][1]) + \
                   abs(scanner_centers[idx][2] - scanner_centers[jdx][2])

            if dist > max_dist:
                max_dist = dist
    print(max_dist)
    interact(local=locals()) 




