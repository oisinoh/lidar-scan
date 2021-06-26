'''
==============
3D scatterplot
==============
Extract data from scanner generated dumpfile and write to plot
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from math import *
import argparse

#setup filename argument parser
parser = argparse.ArgumentParser()                                               

parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

#initialise arrays for use in extracting data
xs,ys,zs,str = ([] for i in range(4))

#open file to be scanned
file = open(args.file,"r")
line = file.readline()
#read each line
while line:
    #parse line
    data = line.split(',')
    #check for correct formatting
    if(len(data) != 4):
        line = file.readline()
        continue
    #load data from line
    theta = radians(int(data[0])) #convert angles to radians
    phi = radians(90 - (int(data[1]) - 90)) # subtract 90 to move to coordinate system
    d = int(data[2])
    s = int(data[3])

    #perform calculations to get x,y,z values
    x = d * sin(phi) * cos(theta)
    y = d * sin(phi) * sin(theta)
    z = d * cos(phi)

    #discard erroneous data points outside of max range of lidar scanner (1200cm)
    if(d > 1200):
        line = file.readline()
        continue
    #add values to corresponding arrays
    xs.append(x)
    ys.append(y)
    zs.append(z)
    str.append(s)
    #continue to next line
    line = file.readline()

#create figure to be plotted
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#reformat strength as numpy array
str_np = np.log(np.array(str))

#create plot
ax.scatter(xs, ys, zs, c=str_np, marker=".")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()