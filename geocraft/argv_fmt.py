# coding: utf-8

import sys

GEO_DIR = "FG-GML-{0:04d}-{1:02d}-DEM5A"
GEO_XML = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"

if len(sys.argv) < 4:
	print("argv_fmt.py area1 area2 subarea")
	exit(-1)

area1 = int(sys.argv[1])
area2 = int(sys.argv[2])
subarea = int(sys.argv[3])

dir = GEO_DIR.format(area1, area2)
fname = GEO_XML.format(area1, area2, subarea)

print("dir=", dir)
print("fname=", fname)
