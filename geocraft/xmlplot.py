# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plot
import sys

GEO_DIR = "FG-GML-{0:04d}-{1:02d}-DEM5A"
GEO_XML = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"

if len(sys.argv) < 4:
	print("xmlplot.py mesh1 mesh2 mesh3 ['grid']")
	exit(-1)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])
mesh3 = int(sys.argv[3])

grid = False
if len(sys.argv) >= 5:
    if sys.argv[4] == 'grid':
        grid = True

dir = GEO_DIR.format(mesh1, mesh2)
fname = GEO_XML.format(mesh1, mesh2, mesh3)

tree = ET.parse(dir+"/"+fname)
root = tree.getroot()

tl = root.find('./{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}DEM/{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}coverage/{http://www.opengis.net/gml/3.2}rangeSet/{http://www.opengis.net/gml/3.2}DataBlock/{http://www.opengis.net/gml/3.2}tupleList')
if tl is None:
    print("{http://www.opengis.net/gml/3.2}tupleList is not found")
    exit(-1)

lines = tl.text.split()
#array = np.zeros(len(lines))
array = np.zeros(33750)
array.fill(-9)
i = 0
for l in lines:
	(t, h) = l.split(",")
	hval = float(h)
	if hval == -9999:
		array[i] = -9
	else:
		array[i] = hval
	i += 1

img_array = array.reshape((150, 225))
if grid:
    gridValue = img_array.max() + 10
    for y in range(0, 150, 30):
        img_array[y:y+1, :] = gridValue
    for x in range(0, 225, 45):
        img_array[:, x:x+1] = gridValue

plot.imshow(img_array)
plot.colorbar()
plot.show()
