# coding: utf-8

import numpy as np
import re
import sys

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"
NPY_DIV5_FILE = "npydiv5-{0:04d}-{1:02d}-{2:02d}.npy"
NPY_FILE = "npy{0}-{1:04d}-{2:02d}-{3:02d}-{4:02d}.npy"

# ここからスタート

if len(sys.argv) < 2:
	print("npydiv5.py npyfilename")
	exit(-1)

m = re.search('npy(data|_5x5)\-([0-9]+)\-([0-9]+)(\-([0-9]+))?(\-([0-9]+))?\.npy', sys.argv[1])
if m is None:
    print("Bad filename")
    exit(-1)

fmt = m.group(1)
mesh1 = int(m.group(2))
mesh2 = int(m.group(3))
mesh3 = None
mesh4 = None

if m.group(5) is not None:
    mesh3 = int(m.group(5))

if m.group(7) is not None:
    mesh4 = int(m.group(7))

if mesh4 is not None:
    print("this file is 4th mesh.")
    exit(-1)

array = np.load(NPY_DIR+"/"+sys.argv[1])

a = np.split(array, 5, axis=1)
#print("a=", a)

count = 0
for j in range(5):
    b = np.split(a[j], 5, axis=0)
    #print("b=", b)
    for i in range(5):
        if mesh3 is None:
            np.save(NPY_DIR+"/"+NPY_DIV5_FILE.format(mesh1, mesh2, count), b[i])
        else:
            np.save(NPY_DIR+"/"+NPY_FILE.format(fmt, mesh1, mesh2, mesh3, count), b[i])
        count+=1
        print(b[i].shape)
