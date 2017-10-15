# coding: utf-8

import numpy as np
import pycra.npydata as nd
import re
import sys

WATER_SURF_FILE = "water-surf.npy"

if len(sys.argv) < 7:
    sys.exit("watersurf.py npfilename hyoukou point_y point_x ymin:ymax xmin:xmax")

hyoukou = None
try:
    hyoukou = float(sys.argv[2])
    #hyoukou -= 0.5
except Exception as err:
    sys.exit("Bad hyoukou. \""+sys.argv[2]+"\"")

print("hyoukou=", hyoukou)

point_y = int(sys.argv[3])
point_x = int(sys.argv[4])

(ymin, ymax) = sys.argv[5].split(":")
(xmin, xmax) = sys.argv[6].split(":")
ymin = int(ymin)
ymax = int(ymax)
xmin = int(xmin)
xmax = int(xmax)

data_array = np.load(nd.NPY_DIR+"/"+sys.argv[1])

(yshape, xshape) = data_array.shape
print("yshape=", yshape, ", xshape=", xshape)

temp_array = np.zeros(data_array.shape)
temp_array.fill(-9999)

start = False
for y in range(point_y, ymax, 1):
    for x in range(xmin, xmax):
        if y == point_y and x == point_x:
            start = True
        if start is True:
            if data_array[y][x] < hyoukou:
                temp_array[y][x] = hyoukou

start = False
for y in range(point_y, ymin, -1):
    for x in range(xmax, xmin-1, -1):
        if y == point_y and x == point_x:
            start = True
        if start is True:
            if data_array[y][x] < hyoukou:
                temp_array[y][x] = hyoukou

np.save(nd.NPY_DIR+"/"+WATER_SURF_FILE, temp_array)
