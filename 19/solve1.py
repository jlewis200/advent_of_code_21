#!/usr/bin/python3

import numpy as np
from itertools import product
from code import interact

file_name = "input"
#file_name = "test_data"

class Sensor:

    transforms = None
    sensors = list()
    sensor_centers = list()
    sensor_centers.append((0,0,0))

    def __init__(self, beacons):
        Sensor.sensors.append(self)
        self.visited = False
        self.beacons = list()
        if Sensor.transforms is None:
            Sensor.transforms = self.get_transforms()

        self.beacons = np.asarray(beacons, dtype=np.int32)

        #get pairwise beacon-to-beacon distances
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

    def get_pairs(self, dst):
        #determine the mapping from source-sensor-beacon-index to destination-sensor-beacon-index
        pairs = list()

        #intersect1d returns the values shared between the 3D arrays
        intersection_set = np.intersect1d(self.dist, dst.dist)

        #a shape of 67 implies the self sensor and the destination sensor have 12 overlapping beacons
        #(12 * 11) / 2 unique pairwise distances
        #this check is optional, but speeds up execution quite a bit because it skips the pairwise comparisons below on 
        #non-overlapping sensors
        if intersection_set.shape[0] == 67: 
            for idx in range(self.dist.shape[0]):
                for jdx in range(dst.dist.shape[0]):
                    #check for 12 identical pairwise-distances using src-beacon-idx and dest-beacon-jdx as the base of 
                    #measurement
                    #this indicates src.beacons[idx] and dst.beacons[jdx] are the same beacon
                    tmp = np.intersect1d(self.dist[idx], dst.dist[jdx])
                    if tmp.shape[0] == 12:
                        pairs.append((idx, jdx))

        return pairs

    def orient_peers(self):
        if self.visited:
            return

        self.visited = True

        for dst in Sensor.sensors:
            if dst.visited :
                continue

            pairs = self.get_pairs(dst)

            if len(pairs) != 12:
                continue

            for transform in Sensor.transforms:
                #apply a transform to dst
                tmp = dst.beacons @ transform
                
                #calculate dst center relative to src based on each beacon
                dst_centers = set()

                for idx, jdx in pairs:
                    dst_centers.add(tuple(self.beacons[idx] - tmp[jdx]))

                #if the number of dst_centers is 1, this indicates the transform was correct
                if len(dst_centers) == 1:
                    #add the scanner_center to the list of scanner centers
                    Sensor.sensor_centers.append(dst_centers.pop())

                    #set the beacons to the transformed orientation and apply the linear offset of the scanner center
                    dst.beacons = tmp + Sensor.sensor_centers[-1] 
                    dst.orient_peers()
                    break


with open(file_name, "r") as in_file:
    sensors = list()
    sensor_datas = in_file.read().split("\n\n")
    
    for sensor_data in sensor_datas:
        beacons = [coord.split(',') for coord in sensor_data.strip().split('\n')[1:]]
        sensors.append(Sensor(beacons))

    sensors[0].orient_peers()
    concatenated = np.concatenate([sensors[idx].beacons for idx in range(len(Sensor.sensors))])
    concat_uniq = np.unique(concatenated, axis=0)
    print(concat_uniq.shape)

    max_dist = 0
    for idx in range(len(sensors) - 1):
        for jdx in range(idx + 1, len(sensors)):
            dist = abs(Sensor.sensor_centers[idx][0] - Sensor.sensor_centers[jdx][0]) + \
                   abs(Sensor.sensor_centers[idx][1] - Sensor.sensor_centers[jdx][1]) + \
                   abs(Sensor.sensor_centers[idx][2] - Sensor.sensor_centers[jdx][2])
     
            if dist > max_dist:
                max_dist = dist

    print(max_dist)

    import code
    code.interact(local=locals())
