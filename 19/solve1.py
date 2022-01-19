#!/usr/bin/python3

import numpy as np
from itertools import product
from code import interact

file_name = "input"
#file_name = "test_data"

class Sensor:

    transforms = None 

    def __init__(self):
        self.oriented = False
        self.beacons = list()
        if Sensor.transforms is None:
            Sensor.transforms = self.get_transforms()

    def add_beacon(self, line):
        self.beacons.append(line.split(","))

    def convert(self):
        """
        Convert beacon list to np array.
        Find all pair-wise inter-beacon distances. 
        """

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

    def get_transforms(self):
        """
        Generate the 24 unique transformation matricies
        """

        #define the basic identity and rotation matrices
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

        #generate the 24 unique transformation matrices
        transforms = list()

        #generate every possible combination of 0-3 rotations about each axis
        for x in range(4):
            for y in range(4):
                for z in range(4):

                    transform = ident.copy()

                    for _ in range(x):
                        transform = rot_x @ transform
                    
                    for _ in range(y):
                        transform = rot_y @ transform

                    for _ in range(z):
                        transform = rot_z @ transform

                    transforms.append(transform.copy())

        #convert to numpy array and retain only the 24 unique transfomation matrices
        transforms = np.asarray(transforms)
        transforms = np.unique(transforms, axis=0)
        return transforms

    def orient(self, sensors, sensor_overlaps, scanner_centers):

        for sensor_overlap in sensor_overlaps:
            if self == sensor_overlap[0] and not sensor_overlap[1].oriented:
                dst = sensor_overlap[1]

            elif self == sensor_overlap[1] and not sensor_overlap[0].oriented:
                dst = sensor_overlap[0]

            else:
                continue

            #determine the mapping from source-sensor-beacon-index to destination-sensor-beacon-index
            pairs = list()

            for idx in range(self.dist.shape[0]):
                for jdx in range(idx, dst.dist.shape[0]):
                    #check for 12 identical pairwise-distances using src-beacon-idx and dest-beacon-jdx as the base of measurement
                    #this indicates src.beacons[idx] and dst.beacons[jdx] are the same beacon
                    tmp = np.intersect1d(self.dist[idx], dst.dist[jdx])
                    if tmp.shape[0] == 12:
                        pairs.append((idx, jdx))

            for transform in Sensor.transforms:
                #apply a transform to dst
                tmp = dst.beacons @ transform
                
                #calculate dst center relative to src based on each beacon
                dst_centers = list()

                for iii, yyy in pairs:
                    dst_centers.append(tuple(self.beacons[iii] - tmp[yyy]))

                #if the number of dst_centers is 1, this indicates the transform was correct
                if len(set(dst_centers)) == 1:
                    #add the scanner_center to the list of scanner centers
                    scanner_centers.append(dst_centers.pop())

                    #set the beacons to the transformed orientation and apply the linear offset of the scanner center
                    dst.beacons = tmp + scanner_centers[-1] 
                    dst.oriented = True
                    dst.orient(sensors, sensor_overlaps, scanner_centers)
                    break


def get_sensors():
    with open(file_name, "r") as in_file:
        
        #build sensor list
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

    return sensors


sensors = get_sensors()
#find sensor-to-sensor overlaps
sensor_overlaps = list()

for idx in range(len(sensors) - 1):
    for jdx in range(idx + 1, len(sensors)):
        #intersect1d returns the number of identical pairwise distances
        tmp = np.intersect1d(sensors[idx].dist, sensors[jdx].dist)
        #67 indicates sensor_overlap:  12*11/2 == 66 + 1 for 0
        if tmp.shape[0] == 67:
            sensor_overlaps.append((sensors[idx], sensors[jdx]))


#this section determines the correct rotation of each sensor relative to sensor 0 and accumulates the unique beacons into a single list
#the complete set tracks which sensor indexes are complete
complete = set()
complete.add(sensors[0])
scanner_centers = [(0,0,0)]
sensor_overlaps = set(sensor_overlaps)

sensors[0].oriented = True
sensors[0].orient(sensors, sensor_overlaps, scanner_centers)
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
#interact(local=locals()) 
