# coding: utf-8

import numpy as np
import matplotlib.pyplot as plot
import pycra.npydata as nd
import sys

# ここからスタート

if len(sys.argv) < 2:
    sys.exit("Usage: plotnpy.py npyfilename [(5x5|10x10)]")

grid = 0
if len(sys.argv) == 3:
    if sys.argv[2] == "5x5":
        grid = 5
    elif sys.argv[2] == "10x10":
        grid = 10

print("grid=", grid)

array = np.load(nd.NPY_DIR+"/"+sys.argv[1])

if grid != 0:
    gridValue = array.max() + 10
    (yshp, xshp) = array.shape
    if yshp >= 1000:
        gridWidth = 5
    else:
        gridWidth = 1
    for y in range(0, yshp, yshp // grid):
        array[y:y+gridWidth, :] = gridValue
    for x in range(0, xshp, xshp // grid):
        array[:, x:x+gridWidth] = gridValue

plot.imshow(array, interpolation='nearest')
plot.colorbar()
plot.show()
