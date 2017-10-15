# coding: utf-8

import numpy as np
import os
import sys

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"

if len(sys.argv) < 6:
    sys.exit("Usage: npycopy.py infile1 infile2 outfile ymin:ymax xmin:xmax")

in1_array = np.load(NPY_DIR+"/"+sys.argv[1])
in2_array = np.load(NPY_DIR+"/"+sys.argv[2])

(ymin, ymax) = sys.argv[4].split(":")
(xmin, xmax) = sys.argv[5].split(":")

in2_array[int(ymin):int(ymax)+1, int(xmin):int(xmax)+1] = in1_array[int(ymin):int(ymax)+1, int(xmin):int(xmax)+1]

np.save(NPY_DIR+"/"+sys.argv[3], in2_array)
