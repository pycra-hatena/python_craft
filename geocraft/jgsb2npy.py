# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plot
import sys

JPGIS_FILE = "JPGIS/5340/L03-b-14_5340-jgd_GML/L03-b-14_5340.xml"

if len(sys.argv) < 2:
    sys.exit("Usage: jgsb2npy.py typeNo")

typeNo = int(sys.argv[1])

tree = ET.parse(JPGIS_FILE)
root = tree.getroot()

for e in root.getiterator():
    print(e.tag)

tl = root.find('./{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}LanduseSubdivisionMesh/{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}coverage/{http://www.opengis.net/gml/3.2}rangeSet/{http://www.opengis.net/gml/3.2}DataBlock/{http://www.opengis.net/gml/3.2}tupleList')
if tl is None:
    raise Exception("{http://www.opengis.net/gml/3.2}tupleList is not found")

lines = tl.text.split("\n")
print("lines=", len(lines))
array = np.empty((800,800), dtype=int)
i = 0
for l in lines:
    print("i=",i)
    d = l.split(" ")
    d.pop(0)
    d = np.array(d, dtype=int)
    print("len(d)=",len(d))
    if len(d) == 800:
        print(d)
        print(len(array[i]))
        array[i] = d
        i += 1

array = 1 * (array == typeNo)

plot.imshow(array, interpolation='nearest')
plot.colorbar()
plot.show()
