# coding: utf-8

import xml.etree.ElementTree as ET
import sys

GEO_DIR = "FG-GML-{0:04d}-{1:02d}-DEM5A"
GEO_XML = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"

if len(sys.argv) < 4:
	print("xmlparse.py mesh1 mesh2 mesh3")
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

print(tl.text)
