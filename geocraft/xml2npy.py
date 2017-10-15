# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import sys
import os

GEO_DIR = "FG-GML-{0:04d}-{1:02d}-DEM5A"
GEO_XML_20161001 = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"
GEO_XML_20170202 = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20170202.xml"

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"
NPY_2ND_FILE = "npydata-{0:04d}-{1:02d}.npy"
NPY_3RD_FILE = "npydata-{0:04d}-{1:02d}-{2:02d}.npy"

WATER_LEVEL = -1.0
SEA_LEVEL = -5.0

def xml2array(mesh1, mesh2, mesh3):
	dir = GEO_DIR.format(mesh1, mesh2)
	fname = GEO_XML_20161001.format(mesh1, mesh2, mesh3)
	if os.path.isfile(dir+"/"+fname) == False:
	    fname = GEO_XML_20170202.format(mesh1, mesh2, mesh3)
	if os.path.isfile(dir+"/"+fname) == False:
	    raise FileNotFoundError(dir+"/"+fname)

	tree = ET.parse(dir+"/"+fname)
	root = tree.getroot()

	tl = root.find('./{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}DEM/{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}coverage/{http://www.opengis.net/gml/3.2}rangeSet/{http://www.opengis.net/gml/3.2}DataBlock/{http://www.opengis.net/gml/3.2}tupleList')
	if tl is None:
		raise Exception("{http://www.opengis.net/gml/3.2}tupleList is not found")

	sp = root.find('./{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}DEM/{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}coverage/{http://www.opengis.net/gml/3.2}coverageFunction/{http://www.opengis.net/gml/3.2}GridFunction/{http://www.opengis.net/gml/3.2}startPoint')
	if sp is None:
		raise Exception("{http://www.opengis.net/gml/3.2}startPoint is not found")

	(spx, spy) = sp.text.split()

	lines = tl.text.split()
	array = np.zeros(33750)
	array.fill(WATER_LEVEL)
	i = int(spx) + int(spy) * 225
	for l in lines:
		(t, h) = l.split(",")
		hval = float(h)
		if hval == -9999:
			array[i] = WATER_LEVEL
		else:
			array[i] = hval
		i += 1

	return array.reshape((150, 225))

# ここからスタート

if len(sys.argv) < 3:
    print("xml2npy.py mesh1 mesh2 [mesh3]")
    exit(-1)

print("sys.argv=", sys.argv)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])

mesh3 = -1

if len(sys.argv) > 3:
    mesh3 = int(sys.argv[3])

print("mesh1=", mesh1)
print("mesh2=", mesh2)
print("mesh3=", mesh3)

if mesh3 == -1:
    yarray = None
    for y in range(10):
        xarray = None
        for x in range(10):
            try:
                m3 = y * 10 + x
                tarray = xml2array(mesh1, mesh2, m3)
            except Excetion as err:
                tarray = np.zeros((150, 225))
                tarray.fill(SEA_LEVEL)
            finally:
                if xarray is None:
                    xarray = tarray
                else:
                    xarray = np.concatenate((xarray, tarray), axis=1)
        if yarray is None:
            yarray = xarray
        else:
            yarray = np.concatenate((xarray, yarray), axis=0)
    np.save(NPY_DIR+"/"+NPY_2ND_FILE.format(mesh1, mesh2), yarray)
else:
    yarray = xml2array(mesh1, mesh2, mesh3)
    np.save(NPY_DIR+"/"+NPY_3RD_FILE.format(mesh1, mesh2, mesh3), yarray)

print(yarray.shape)
