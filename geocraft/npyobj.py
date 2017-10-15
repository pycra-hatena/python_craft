# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import re
import sys


NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"
NPY_FILENAME = "npyobj({:d}){}"

if len(sys.argv) < 2:
    sys.exit("Usage: npyobj.py npyfilename [shubetsu] [minsize] [plot]")

shubetsu = 3    # 3=内水面
if len(sys.argv) >= 3:
    shubetsu = int(sys.argv[2])

minsize = 1
if len(sys.argv) >= 4:
    minsize = int(sys.argv[3])

plot = False
if len(sys.argv) >= 5:
    if sys.argv[4] == 'plot':
        plot = True

m = re.search('npysurf((\-[0-9]+)+)\.npy', sys.argv[1])
if m is None:
    sys.exit("Bad filename")

array = np.load(NPY_DIR+"/"+sys.argv[1])
array = 1 * (array == shubetsu)

im_open = scipy.ndimage.binary_opening(array, np.ones((minsize, minsize)), iterations=2)
label, num_features = scipy.ndimage.measurements.label(im_open)
print("num_features=", num_features)

if num_features == 0:
    sys.exit("No object")

np.save(NPY_DIR+"/"+NPY_FILENAME.format(num_features, m.group(1)), label)

if plot == False:
    sys.exit(0)

plt.subplot(211)
plt.imshow(array, cmap='Greys_r')
plt.colorbar()
plt.subplot(212)
plt.imshow(label, cmap='Greys_r')
plt.colorbar()
plt.show()
