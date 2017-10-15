# coding: utf-8

import numpy as np
import re
import os
import sys

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"
SURF_FILENAME = "npysurf-{0:04d}-{1:02d}-{2:02d}.npy"
DATA_FILENAME = "npydata-{0:04d}-{1:02d}-{2:02d}.npy"
TEMP_LAKE_FILENAME = "temp_lake-{0:04d}-{1:02d}-{2:02d}-{3:d}-{4:d}.npy"
TEMP_DATA_FILENAME = "temp_data-{0:04d}-{1:02d}-{2:02d}-{3:d}-{4:d}.npy"
TEMP_SURF_FILENAME = "temp_surf-{0:04d}-{1:02d}-{2:02d}-{3:d}-{4:d}.npy"
LOG_FILENAME = "log_objlake.txt"

if len(sys.argv) < 4:
    sys.exit("Usage: objlake.py npyobjfilename objno depth")

print("npyobjfilename=", sys.argv[1])

if os.path.isfile(NPY_DIR+"/"+sys.argv[1]) == False:
    sys.exit("Object File not found.")

m = re.search('npyobj\(([0-9]+)\)\-([0-9]+)\-([0-9]+)\-([0-9]+)\.npy', sys.argv[1])

if m is None:
    sys.exit("Bad filename")

print(m.group(1))
print(m.group(2))
print(m.group(3))
print(m.group(4))

num_obj = int(m.group(1))
mesh1 = int(m.group(2))
mesh2 = int(m.group(3))
mesh3 = int(m.group(4))

objno = int(sys.argv[2])
if objno > num_obj:
    sys.exit("Bad objno")

depth = int(sys.argv[3])
if depth == 0:
    sys.exit("Bad depth")

if os.path.isfile(NPY_DIR+"/"+DATA_FILENAME.format(mesh1, mesh2, mesh3)) == False:
    sys.exit("Data File not found.")

if os.path.isfile(NPY_DIR+"/"+SURF_FILENAME.format(mesh1, mesh2, mesh3)) == False:
    sys.exit("Surface File not found.")

print("Go!")

obj_array = np.load(NPY_DIR+"/"+sys.argv[1])
data_array = np.load(NPY_DIR+"/"+DATA_FILENAME.format(mesh1, mesh2, mesh3))
surf_array = np.load(NPY_DIR+"/"+SURF_FILENAME.format(mesh1, mesh2, mesh3))

border_val = data_array.max() + 10
obj_cell = 0
ymin = obj_array.shape[0]
ymax = 0
xmin = obj_array.shape[1]
xmax = 0
pos1st_y = -1
pos1st_x = -1

#print("obj_cell=", obj_cell)
#print("ymin=", ymin, ", ymax=", ymax)
#print("xmin=", xmin, ", xmax=", xmax)
#print("pos1st_y=", pos1st_y, "pos1st_x=", pos1st_x)

for y in range(obj_array.shape[0]):
    for x in range(obj_array.shape[1]):
        if obj_array[y][x] == objno:
            obj_cell += 1
            if pos1st_y == -1:
                pos1st_y = y
                pos1st_x = x
            if y > ymax:
                ymax = y
            if y < ymin:
                ymin = y
            if x > xmax:
                xmax = x
            if x < xmin:
                xmin = x

print("obj_cell=", obj_cell)
print("ymin=", ymin, ", ymax=", ymax)
print("xmin=", xmin, ", xmax=", xmax)
print("pos1st_y=", pos1st_y, "pos1st_x=", pos1st_x)

surf_val = surf_array.max() + 2
data_min = data_array.max()
for y in range(ymin, ymax+1):
    for x in range(xmin, xmax+1):
        if obj_array[y][x] == objno:
            if surf_array[y-1][x] == 5: # 上 5=地表面
                if data_min > data_array[y-1][x]:
                    data_min = data_array[y-1][x]
                surf_array[y-1][x] = surf_val
            if surf_array[y+1][x] == 5: # 下 5=地表面
                if data_min > data_array[y+1][x]:
                    data_min = data_array[y+1][x]
                surf_array[y+1][x] = surf_val
            if surf_array[y][x-1] == 5: # 左 5=地表面
                if data_min > data_array[y][x-1]:
                    data_min = data_array[y][x-1]
                surf_array[y][x-1] = surf_val
            if surf_array[y][x+1] == 5: # 左 5=地表面
                if data_min > data_array[y][x+1]:
                    data_min = data_array[y][x+1]
                surf_array[y][x+1] = surf_val

print("data_min=", data_min)

bottom_val = data_min - depth
print("bottom_val=", bottom_val)
for y in range(ymin, ymax+1):
    for x in range(xmin, xmax+1):
        if obj_array[y][x] == objno:
            data_array[y][x] = bottom_val

np.save(NPY_DIR+"/"+TEMP_LAKE_FILENAME.format(mesh1, mesh2, mesh3, objno, depth), data_array)

if obj_cell > 0:
    #data_array[ymin-1:ymax+1, xmin-1:xmin] = border_val
    #data_array[ymin-1:ymax+1, xmax:xmax+1] = border_val
    #data_array[ymin-1:ymin, xmin-1:xmax] = border_val
    #data_array[ymax:ymax+1, xmin-1:xmax] = border_val
    data_array[ymin-2:ymax+2, xmin-2:xmin-1] = border_val
    data_array[ymin-2:ymax+2, xmax+2:xmax+3] = border_val
    data_array[ymin-2:ymin-1, xmin-2:xmax+3] = border_val
    data_array[ymax+2:ymax+3, xmin-2:xmax+3] = border_val
    np.save(NPY_DIR+"/"+TEMP_DATA_FILENAME.format(mesh1, mesh2, mesh3, objno, depth), data_array)
    np.save(NPY_DIR+"/"+TEMP_SURF_FILENAME.format(mesh1, mesh2, mesh3, objno, depth), surf_array)

with open(NPY_DIR+"/"+LOG_FILENAME, 'a') as f:
    for p in sys.argv:
        f.write("{} ".format(p))
    f.write("\n")
    f.write("{0}={1:d}\n".format('obj_cell', obj_cell))
    f.write("{0}={1:d}, {2}={3:d}\n".format('ymin', ymin, 'ymax', ymax))
    f.write("{0}={1:d}, {2}={3:d}\n".format('xmin', xmin, 'xmax', xmax))
    f.write("{0}={1:d}, {2}={3:d}\n".format('pos1st_y', pos1st_y, 'pos1st_x', pos1st_x))
    f.write("{0}={1}\n".format('data_min', data_min))
    f.write("{0}={1}\n".format('bottom_val', bottom_val))
    f.write("{0}=\"{1}\"\n".format('temp_data_file', NPY_DIR+"/"+TEMP_DATA_FILENAME.format(mesh1, mesh2, mesh3, objno, depth)))
    f.write("{0}=\"{1}\"\n".format('temp_surf_file', NPY_DIR+"/"+TEMP_SURF_FILENAME.format(mesh1, mesh2, mesh3, objno, depth)))
    f.write("{0}=\"{1}\"\n".format('temp_lake_file', NPY_DIR+"/"+TEMP_LAKE_FILENAME.format(mesh1, mesh2, mesh3, objno, depth)))
    f.write("\n")

