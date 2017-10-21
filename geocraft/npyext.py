# coding: utf-8

import numpy as np
import pycra.npydata as nd
import sys

if len(sys.argv) < 4:
    sys.exit("npyext.py npyfilename ymin:ymax xmin:xmax")

(ymin, ymax) = sys.argv[2].split(":")
(xmin, xmax) = sys.argv[3].split(":")

array = np.load(nd.NPY_DIR+"/"+sys.argv[1])

extarray = array[int(ymin):int(ymax), int(xmin):int(xmax)].copy()  # 実体

np.save(nd.NPY_DIR+"/extract.npy", extarray)
