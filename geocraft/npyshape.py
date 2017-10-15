# coding: utf-8

import numpy as np
import sys

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"

if len(sys.argv) < 2:
    print("npyshape.py npyfilename")
    exit(-1)

array = np.load(NPY_DIR+"/"+sys.argv[1])

print(array.shape)
