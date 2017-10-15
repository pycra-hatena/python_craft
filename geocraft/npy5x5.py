# coding: utf-8

import numpy as np
from scipy.ndimage import filters
import re
import sys

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"
NPY_FILE = "npy_5x5{0}.npy"

# ここからスタート

if len(sys.argv) < 2:
	print("npyall.py npyfilename")
	exit(-1)

m = re.search('npy(data|_5x5|lake)((\-[0-9]+)+)\.npy', sys.argv[1])
if m is None:
    print("Bad npy filename.")
    exit(-1)

if m.group(1) == '_5x5':
    print("This is 5x5 file.")
    exit(-1)

array = np.load(NPY_DIR+"/"+sys.argv[1])
print(array.shape)
print(array)
array5 = np.repeat(array, 5, axis=0)
print(array5.shape)
print(array5)
array5x5 = np.repeat(array5, 5, axis=1)
print(array5x5.shape)
print(array5x5)
aa_array = filters.gaussian_filter(array5x5, 2)

np.save(NPY_DIR+"/"+NPY_FILE.format(m.group(2)), aa_array)
