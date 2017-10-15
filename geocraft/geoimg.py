# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

GEO_OFFSET = 30

GEO_DIR_DIC = {
	"5340":"FG-GML-5340-22-DEM5A", # 大網白里
	"5239":"FG-GML-5239-73-DEM5A", # 茅ヶ崎（海側）
	"5339":"FG-GML-5339-03-DEM5A", # 茅ヶ崎（陸側）
	"5438":"FG-GML-5438-00-DEM5A"  # 諏訪湖
	}

GEO_XML_DIC = {
	"5340":"FG-GML-5340-22-{0:02d}-DEM5A-20161001.xml", # 大網白里
	"5239":"FG-GML-5239-73-{0:02d}-DEM5A-20161001.xml", # 茅ヶ崎（海側）
	"5339":"FG-GML-5339-03-{0:02d}-DEM5A-20161001.xml", # 茅ヶ崎（陸側）
	"5438":"FG-GML-5438-00-{0:02d}-DEM5A-20161001.xml"  # 諏訪湖
	}

# 大網白里
#GEO_DIR = "FG-GML-5340-22-DEM5A"
#GEO_XML = "FG-GML-5340-22-{0:02d}-DEM5A-20161001.xml"
# 茅ヶ崎（海側）
#GEO_DIR = "FG-GML-5239-73-DEM5A"
#GEO_XML = "FG-GML-5239-73-{0:02d}-DEM5A-20161001.xml"
# 茅ヶ崎（陸側）
#GEO_DIR = "FG-GML-5339-03-DEM5A"
#GEO_XML = "FG-GML-5339-03-{0:02d}-DEM5A-20161001.xml"
# 諏訪湖
#GEO_DIR = "FG-GML-5438-00-DEM5A"
#GEO_XML = "FG-GML-5438-00-{0:02d}-DEM5A-20161001.xml"

IMG_DIR = "/Users/sakai/Desktop/GEO_IMAGE"
IMG_NAME = "geoimg-{0:02d}.png"
unit_width = 225
unit_height = 150

def geo2array(fname):
	tree = ET.parse(GEO_DIR+"/"+fname)
	root = tree.getroot()
	
	ge = root.find('./{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}DEM/{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}coverage/{http://www.opengis.net/gml/3.2}gridDomain/{http://www.opengis.net/gml/3.2}Grid/{http://www.opengis.net/gml/3.2}limits/{http://www.opengis.net/gml/3.2}GridEnvelope')
	if ge is None:
		print("{http://www.opengis.net/gml/3.2}GridEnvelope is not found")
		raise RuntimeError()
	
	ge_low = ge.find('{http://www.opengis.net/gml/3.2}low')
	if ge_low is None:
		print("{http://www.opengis.net/gml/3.2}low is not found")
		raise RuntimeError()
	
	ge_low_values = ge_low.text.split()
	ge_high = ge.find('{http://www.opengis.net/gml/3.2}high')
	if ge_high is None:
		print("{http://www.opengis.net/gml/3.2}high is not found")
		raise RuntimeError()
	
	ge_high_values = ge_high.text.split()
	
	tl = root.find('./{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}DEM/{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}coverage/{http://www.opengis.net/gml/3.2}rangeSet/{http://www.opengis.net/gml/3.2}DataBlock/{http://www.opengis.net/gml/3.2}tupleList')
	if tl is None:
		print("{http://www.opengis.net/gml/3.2}tupleList is not found")
		raise RuntimeError()
	
	lines = tl.text.split()
	high_size = [int(ge_high_values[1])-int(ge_low_values[1])+1, int(ge_high_values[0])-int(ge_low_values[0])+1]
	
	data1 = np.empty(high_size[0]*high_size[1])
	i = 0
	for l in lines:
		parts = l.split(",")
		if parts[0] == u"地表面":
			data1[i] = float(parts[1]) + GEO_OFFSET
		elif parts[0] == u"内水面":
			data1[i] = 0
		elif parts[0] == u"海水面":
			data1[i] = 0
		else:
			data1[i] = 0
			print(parts[0])
		i += 1
		if i >= high_size[0]*high_size[1]:
			break

	high_array = data1.reshape(high_size)
	return high_array

tarray = np.zeros([unit_height*10, unit_width*10])
pos_x = 0
pos_y = 0
for i in range(100):
	try:
		fname = GEO_XML.format(i)
		print(fname)
		harray = geo2array(fname)
		unit_y = int(i / 10)
		unit_x = i % 10
		#print(unit_y, unit_x)
		pos_x = unit_x * unit_width
		pos_y = (9 - unit_y) * unit_height
		#print(pos_y, pos_x)
		for y in range(unit_height):
			for x in range(unit_width):
				tarray[y+pos_y][x+pos_x] = harray[y][x]
	except FileNotFoundError as e:
		print("FileNotFound ", e.strerror)
	except RuntimeError as e:
		print("RuntimeError ", e.strerror)

pil_im = Image.fromarray(np.uint8(tarray))
pil_im.save(IMG_DIR+"/"+"geo_image.png", 'PNG', quality=100, optimize=True)
