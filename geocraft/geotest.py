# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import sys

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

IMG_DIR = "/Users/sakai/Desktop/GEO_IMAGE"
IMG_NAME = "geoimg-{0:04d}-{1:02d}.png"

def geo2array(fdir, fname):
	tree = ET.parse(fdir+"/"+fname)
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
	last_hight = 0
	i = 0
	for l in lines:
		parts = l.split(",")
		if parts[0] == u"地表面":
			last_high = float(parts[1]) #* 0.2
			data1[i] = last_high
		elif parts[0] == u"内水面":
			data1[i] = last_high - 1
		elif parts[0] == u"海水面":
			data1[i] = last_high - 1
		else:
			data1[i] = last_high - 1
			print(parts[0])
		i += 1
		if i >= high_size[0]*high_size[1]:
			break

	high_array = data1.reshape(high_size)
	return high_array


print(sys.argv)

if len(sys.argv) < 2:
	print("geotest.py 地域番号 [マップNo.] [255(255マッピング)]")
	exit(-1)

key1 = ""
if len(sys.argv) >= 2:
	key1 = sys.argv[1]

if key1 not in GEO_DIR_DIC:
	print("\"", key1, "\"は指定できません。")
	exit(-1)

key2 = 0
if len(sys.argv) >= 3:
	key2 = int(sys.argv[2])

key3 = 0
if len(sys.argv) >= 4:
	key3 = int(sys.argv[3])

dir = GEO_DIR_DIC[key1]
print(dir)

xmlfmt = GEO_XML_DIC[key1]
xml = xmlfmt.format(key2)
print(xml)

try:
	harray = geo2array(dir, xml)
	hmax = harray.max()
	print("hmax=", hmax)
	hmin = harray.min()
	print("hmin=", hmin)
	if key3 == 255:
		tarray = ((harray - hmin) / (hmax - hmin)) * 255
	else:
		tarray = harray
except FileNotFoundError as e:
	print("FileNotFound ", e.strerror)
except RuntimeError as e:
	print("RuntimeError ", e.strerror)

pil_im = Image.fromarray(np.uint8(tarray))
pil_im.save(IMG_DIR+"/"+IMG_NAME.format(int(key1), key2), 'PNG', quality=100, optimize=True)

