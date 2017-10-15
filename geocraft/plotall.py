# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plot
import sys
import os.path

GEO_DIR = "FG-GML-{0:04d}-{1:02d}-DEM5A"
GEO_XML_20161001 = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"
GEO_XML_20170202 = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20170202.xml"

def xml2array(mesh1, mesh2, mesh3):
	dir = GEO_DIR.format(mesh1, mesh2)
	fname = GEO_XML_20161001.format(mesh1, mesh2, mesh3)
	if os.path.isfile(dir+"/"+fname) == False:
	    fname = GEO_XML_20170202.format(mesh1, mesh2, mesh3)

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

	return array.reshape((150, 225))


# ここからスタート

if len(sys.argv) < 3:
	print("plotall.py mesh1 mesh2 ['grid']")
	exit(-1)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])

grid = False
if len(sys.argv) >= 4:
    if sys.argv[3] == 'grid':
        grid = True

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
			array.fill(-10)
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

# 部分的に抽出
#parray = yarray[950:1400, 150:750] # ビュー
#parray = yarray[950:1400, 150:750].copy()  # 実体
if grid:
    gridValue = yarray.max() + 10
    for y in range(0, yarray.shape[0], 150):
        yarray[y:y+3, :] = gridValue
    for x in range(0, yarray.shape[1], 225):
        yarray[:, x:x+3] = gridValue

plot.imshow(yarray)
plot.colorbar()
plot.show()
