# coding: utf-8

import numpy as np
import sys

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"

if len(sys.argv) < 4:
    print("npyext.py npyfilename ymin:ymax xmin:xmax")
    exit(-1)

(ymin, ymax) = sys.argv[2].split(":")
(xmin, xmax) = sys.argv[3].split(":")

array = np.load(NPY_DIR+"/"+sys.argv[1])

extarray = array[int(ymin):int(ymax), int(xmin):int(xmax)].copy()  # 実体

np.save(NPY_DIR+"/extract.npy", extarray)
