# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plot
import sys

GEO_DIR = "FG-GML-{0:04d}-{1:02d}-DEM5A"
GEO_XML = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"

NPY_DIR = "/Users/sakai/Desktop"
NPY_FILE = "npydata-{0:04d}-{1:02d}.npy"

WATER_LEVEL = -1.0
SEA_LEVEL = -5.0

def xml2array(mesh1, mesh2, mesh3):
	dir = GEO_DIR.format(mesh1, mesh2)
	fname = GEO_XML.format(mesh1, mesh2, mesh3)

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
	print("npyall.py mesh1 mesh2")
	exit(-1)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])

yarray = None
for y in range(10):
	xarray = None
	for x in range(10):
		try:
			mesh3 = y * 10 + x
			array = xml2array(mesh1, mesh2, mesh3)
		except Exception as err:
			print(err)
			array = np.zeros((150, 225))
			array.fill(SEA_LEVEL)
		finally:
			if xarray is None:
				xarray = array
			else:
				xarray = np.concatenate((xarray, array), axis=1)
		
	if yarray is None:
		yarray = xarray
	else:
		yarray = np.concatenate((xarray, yarray), axis=0)

print(yarray.shape)

# 部分的に抽出（DASH島）
#parray = yarray[950:1400, 150:750] # ビュー
parray = yarray[950:1400, 150:750].copy()  # 実体

np.save(NPY_DIR+"/"+NPY_FILE.format(mesh1, mesh2), parray)

plot.imshow(parray)
plot.colorbar()
plot.show()
