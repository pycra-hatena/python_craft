# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
from scipy.ndimage import filters
import matplotlib.pyplot as plot
import sys

GEO_DIR = "FG-GML-{0:04d}-{1:02d}-DEM5A"
GEO_XML = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"

NPY_DIR = "/Users/sakai/Desktop"
NPY_FILE = "npydata-{0:04d}-{1:02d}-{2:02d}.npy"

if len(sys.argv) < 4:
    print("xmlnpy.py mesh1 mesh2 mesh3")
    exit(-1)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])
mesh3 = int(sys.argv[3])

dir = GEO_DIR.format(mesh1, mesh2)
fname = GEO_XML.format(mesh1, mesh2, mesh3)

tree = ET.parse(dir+"/"+fname)
root = tree.getroot()

tl = root.find('./{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}DEM/{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}coverage/{http://www.opengis.net/gml/3.2}rangeSet/{http://www.opengis.net/gml/3.2}DataBlock/{http://www.opengis.net/gml/3.2}tupleList')
if tl is None:
    print("{http://www.opengis.net/gml/3.2}tupleList is not found")
    exit(-1)

sp = root.find('./{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}DEM/{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}coverage/{http://www.opengis.net/gml/3.2}coverageFunction/{http://www.opengis.net/gml/3.2}GridFunction/{http://www.opengis.net/gml/3.2}startPoint')
if sp is None:
    print("{http://www.opengis.net/gml/3.2}startPoint is not found")
    exit(-1)

(spx, spy) = sp.text.split()

lines = tl.text.split()
array = np.zeros(33750)
array.fill(-9)
i = int(spx) + int(spy) * 225
for l in lines:
    (t, h) = l.split(",")
    hval = float(h)
    if hval == -9999:
        array[i] = -9
    else:
        array[i] = hval
    i += 1

data_array = array.reshape((150, 225))
print(data_array.shape)
print(data_array)
data5_array = np.repeat(data_array, 5, axis=0)
print(data5_array.shape)
print(data5_array)
data5x5_array = np.repeat(data5_array, 5, axis=1)
print(data5x5_array.shape)
print(data5x5_array)
aa_array = filters.gaussian_filter(data5x5_array, 2)
#plot.imshow(aa_array)
#plot.colorbar()
#plot.show()
np.save(NPY_DIR+"/"+NPY_FILE.format(mesh1, mesh2, mesh3), aa_array)
