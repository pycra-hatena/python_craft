# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plot
import sys


JPGIS_FILE = "JPGIS/5340/L03-a-14_5340-jgd_GML/L03-a-14_5340.xml"

tree = ET.parse(JPGIS_FILE)
root = tree.getroot()

for e in root.getiterator():
    print(e.tag)

tl = root.find('./{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}LanduseMesh/{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}coverage/{http://www.opengis.net/gml/3.2}rangeSet/{http://www.opengis.net/gml/3.2}DataBlock/{http://www.opengis.net/gml/3.2}tupleList')
if tl is None:
    raise Exception("{http://www.opengis.net/gml/3.2}tupleList is not found")

temp = np.array([[107, 66, 0], [221, 148, 0], [71, 104, 33], [255, 208, 138],
    [196, 44, 0], [162, 162, 162], [116, 116, 116], [48, 48, 48],
    [132, 183, 255], [72, 157, 255], [0, 86, 185], [163, 215, 113], [255, 255, 255]], dtype=float)
temp = temp / 255.0
lines = tl.text.split()
array = np.zeros((6400, 3))
i = 0
for l in lines:
    d = np.array(l.split(","), np.float)
    s = sum(d)
    d = d / s
    total = np.zeros((3), dtype=float)
    for j in range(13):
        t = d[j] * temp[j]
        total = total + t
    #print(total)
    array[i] = total
    i += 1

print(array)
array = array.reshape((80, 80, 3))
print(array)

plot.imshow(array, interpolation='nearest')
plot.show()
