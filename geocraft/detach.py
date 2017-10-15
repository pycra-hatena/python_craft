# coding: utf-8

import numpy as np
import matplotlib.pyplot as plot
import pycra.npydata as nd
import sys

L03B_FORMAT = "npyl03-b-{0:04d}.npy"
L03B_MESH2_FORMAT = "npyl03-b-{0:04d}-{1:02d}.npy"
L03B_MESH3_FORMAT = "npyl03-b-{0:04d}-{1:02d}-{2:02d}.npy"

if len(sys.argv) < 3:
    sys.exit("Usage: detach.py mesh1 mesh2 [mesh3]")

print(sys.argv)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])

mesh3 = None
if len(sys.argv) >= 4:
    mesh3 = int(sys.argv[3])

array = np.load(nd.NPY_DIR+"/"+L03B_FORMAT.format(mesh1))

min_y = 0
min_x = 0
(max_y, max_x) = array.shape

max_y = max_y - (mesh2 // 10) * 100
min_y = max_y - 100
min_x = (mesh2 % 10) * 100
max_x = min_x + 100
print("min_y=", min_y)
print("max_y=", max_y)
print("min_x=", min_x)
print("max_x=", max_x)

if mesh3 is None:
    out_array = array[min_y:max_y, min_x:max_x]
    array15 = np.repeat(out_array, 15, axis=0)
    array15x23 = np.repeat(array15, 23, axis=1)
    del_collect = []
    for i in range(50):
        del_collect.append((i+1)*46-1)
    out_array = np.delete(array15x23, del_collect, 1)
    np.save(nd.NPY_DIR+"/"+L03B_MESH2_FORMAT.format(mesh1, mesh2), out_array)
else:
    max_yy = max_y - (mesh3 // 10) * 10
    min_yy = max_yy - 10
    min_xx = min_x + (mesh3 % 10) * 10
    max_xx = min_xx + 10
    print("min_yy=", min_yy)
    print("max_yy=", max_yy)
    print("min_xx=", min_xx)
    print("max_xx=", max_xx)
    out_array = array[min_yy:max_yy, min_xx:max_xx]
    print(out_array)
    array15 = np.repeat(out_array, 15, axis=0)
    array15x23 = np.repeat(array15, 23, axis=1)
    del_collect = []
    for i in range(5):
        del_collect.append((i+1)*46-1)
    out_array = np.delete(array15x23, del_collect, 1)
    np.save(nd.NPY_DIR+"/"+L03B_MESH3_FORMAT.format(mesh1, mesh2, mesh3), out_array)

print(out_array.shape)

plot.imshow(out_array, interpolation='nearest')
plot.colorbar()
plot.show()
