# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import sys


NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"

if len(sys.argv) < 2:
    print("buttai.py npyfilename")
    exit(-1)

array = np.load(NPY_DIR+"/"+sys.argv[1])
array = 1 * (array == 3)    # 3=池

im_open = scipy.ndimage.binary_opening(array, np.ones((3, 3)), iterations=2)
label3, num_features = scipy.ndimage.measurements.label(im_open)
print("label3=", label3)
print("num_features=", num_features)

im_open = scipy.ndimage.binary_opening(array, np.ones((2, 2)), iterations=2)
label2, num_features = scipy.ndimage.measurements.label(im_open)
print("label2=", label2)
print("num_features=", num_features)

im_open = scipy.ndimage.binary_opening(array, np.ones((1, 1)), iterations=2)
label1, num_features = scipy.ndimage.measurements.label(im_open)
print("label1=", label1)
print("num_features=", num_features)

plt.subplot(221)
plt.imshow(array, cmap='Greys_r')
plt.colorbar()
plt.subplot(222)
plt.imshow(label3, cmap='Greys_r')
plt.colorbar()
plt.subplot(223)
plt.imshow(label2, cmap='Greys_r')
plt.colorbar()
plt.subplot(224)
plt.imshow(label1, cmap='Greys_r')
plt.colorbar()
plt.show()
