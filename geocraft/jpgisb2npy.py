# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plot
import pycra.npydata as nd
import sys

JPGIS_FILE = "JPGIS/5340/L03-b-14_5340-jgd_GML/L03-b-14_5340.xml"
NPYL03B_5340_FILE = "npyl03-b-5340.npy"

tree = ET.parse(JPGIS_FILE)
root = tree.getroot()

for e in root.getiterator():
    print(e.tag)

tl = root.find('./{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}LanduseSubdivisionMesh/{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}coverage/{http://www.opengis.net/gml/3.2}rangeSet/{http://www.opengis.net/gml/3.2}DataBlock/{http://www.opengis.net/gml/3.2}tupleList')
if tl is None:
    raise Exception("{http://www.opengis.net/gml/3.2}tupleList is not found")

lines = tl.text.split("\n")
array = np.empty((800,800), dtype=int)
i = 0
for l in lines:
    d = l.split(" ")
    d.pop(0)
    d = np.array(d, dtype=int)
    if len(d) == 800:
        array[i] = d
        i += 1

np.save(nd.NPY_DIR+"/"+NPYL03B_5340_FILE, array)

plot.imshow(array, interpolation='nearest')
plot.colorbar()
plot.show()
