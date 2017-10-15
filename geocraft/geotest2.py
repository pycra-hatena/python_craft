# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from scipy.ndimage import filters
import sys

GEO_OFFSET = 30

#GEO_DIR_DIC = {
#	"5340":"FG-GML-5340-22-DEM5A", # 大網白里
#	"5239":"FG-GML-5239-73-DEM5A", # 茅ヶ崎（海側）
#	"5339":"FG-GML-5339-03-DEM5A", # 茅ヶ崎（陸側）
#	"5438":"FG-GML-5438-00-DEM5A"  # 諏訪湖
#	}
GEO_DIR_FORMAT = "FG-GML-{0:04d}-{1:02d}-DEM5A"

#GEO_XML_DIC = {
#	"5340-22":"FG-GML-5340-22-{0:02d}-DEM5A-20161001.xml", # 大網白里
#	"5239-73":"FG-GML-5239-73-{0:02d}-DEM5A-20161001.xml", # 茅ヶ崎（海側）
#	"5339-03":"FG-GML-5339-03-{0:02d}-DEM5A-20161001.xml", # 茅ヶ崎（陸側）
#	"5438-00":"FG-GML-5438-00-{0:02d}-DEM5A-20161001.xml"  # 諏訪湖
#	}
GEO_XML_FORMAT = "FG-GML-{0:04d}-{1:02d}-{2:02d}-DEM5A-20161001.xml"

IMG_DIR = "/Users/sakai/Desktop/GEO_IMAGE"
IMG_NAME = "geoimg-{0:04d}-{1:02d}-{2:02d}.png"
IMG_NAME_SPLIT = "geoimg-{0:04d}-{1:02d}-{2:02d}-{3:02d}.png"
TYPE_NAME_SPLIT = "geotyp-{0:04d}-{1:02d}-{2:02d}.npy"
NPY_NAME_SPLIT = "geonpy-{0:04d}-{1:02d}-{2:02d}-{3:02d}.npy"

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
	
	data_type = np.empty(high_size[0]*high_size[1])
	data1 = np.empty(high_size[0]*high_size[1])
	last_hight = 0
	i = 0
	for l in lines:
		parts = l.split(",")
		if parts[0] == u"地表面":
			last_high = float(parts[1]) #* 0.2
			data1[i] = last_high
			data_type[i] = 1
		elif parts[0] == u"内水面":
			data1[i] = last_high - 1
			data_type[i] = 2
		elif parts[0] == u"海水面":
			data1[i] = last_high - 1
			data_type[i] = 3
		else:
			data1[i] = last_high - 1
			data_type[i] = 0
			print(parts[0])
		i += 1
		if i >= high_size[0]*high_size[1]:
			break

	high_array = data1.reshape(high_size)
	type_array = data_type.reshape(high_size)
	return (high_array, type_array)


print(sys.argv)

if len(sys.argv) < 2:
	print("geotest2.py 地域番号 地域サブ番号 [マップNo.] [255(255マッピング)|5x5]")
	exit(-1)

key1 = 0
if len(sys.argv) >= 3:
	key1 = int(sys.argv[1])

key2 = 0
if len(sys.argv) >= 3:
	key2 = int(sys.argv[2])

key3 = 0
if len(sys.argv) >= 4:
	key3 = int(sys.argv[3])

key4 = ""
if len(sys.argv) >= 5:
	key4 = sys.argv[4]

dir = GEO_DIR_FORMAT.format(key1, key2)
print(dir)

xml = GEO_XML_FORMAT.format(key1, key2, key3)
print(xml)

try:
	harray, tdata = geo2array(dir, xml)
	hshape = harray.shape
	print("hshape=", hshape)
	hmax = harray.max()
	print("hmax=", hmax)
	hmin = harray.min()
	print("hmin=", hmin)
	if key4 == "255":
		tarray = ((harray - hmin) / (hmax - hmin)) * 255
	elif key4 == "5x5":
		hshape = harray.shape
		tarray = np.zeros((hshape[0]*5, hshape[1]*5))
		print("tarray.shape=", tarray.shape)
		for z in range(hshape[0]):
			for x in range(hshape[1]):
				for zz in range(5):
					for xx in range(5):
						tarray[z*5+zz][x*5+xx] = harray[z][x]
		# フィルタリング
		tshape = tarray.shape
		t2array = tarray.copy()
		if True:
			tarray = filters.gaussian_filter(t2array, 2)
		else:
			for z in range(2, tshape[0]-2):
				for x in range(2, tshape[1]-2):
					tval = 0
					tval += t2array[z-2][x-2] * 0.125
					tval += t2array[z-2][x-1] * 0.25
					tval += t2array[z-2][x] * 0.25
					tval += t2array[z-2][x+1] * 0.25
					tval += t2array[z-2][x+2] * 0.125
					tval += t2array[z-1][x-2] * 0.25
					tval += t2array[z-1][x-1] * 0.5
					tval += t2array[z-1][x] * 0.5
					tval += t2array[z-1][x+1] * 0.5
					tval += t2array[z-1][x+2] * 0.25
					tval += t2array[z][x-2] * 0.25
					tval += t2array[z][x-1] * 0.5
					tval += t2array[z][x] * 1.0
					tval += t2array[z][x+1] * 0.5
					tval += t2array[z][x+2] * 0.25
					tval += t2array[z+1][x-2] * 0.25
					tval += t2array[z+1][x-1] * 0.5
					tval += t2array[z+1][x] * 0.5
					tval += t2array[z+1][x+1] * 0.5
					tval += t2array[z+1][x+2] * 0.25
					tval += t2array[z+2][x-2] * 0.125
					tval += t2array[z+2][x-1] * 0.25
					tval += t2array[z+2][x] * 0.25
					tval += t2array[z+2][x+1] * 0.25
					tval += t2array[z+2][x+2] * 0.125
					tarray[z][x] = tval / 8.5
	else:
		tarray = harray
except FileNotFoundError as e:
	print("FileNotFound ", e.strerror)
except RuntimeError as e:
	print("RuntimeError ", e.strerror)

t2array = tarray.copy()
pil_im = Image.fromarray(np.uint8(t2array))
pil_im.save(IMG_DIR+"/"+IMG_NAME.format(key1, key2, key3), 'PNG', quality=100, optimize=True)

if key4 == "5x5":
	np.save(IMG_DIR+"/"+TYPE_NAME_SPLIT.format(key1, key2, key3), tdata)
	count = 0
	splarrays = np.split(tarray, 5, axis=0)
	#print(splarrays)
	for i in range(5):
		hsparrays = np.split(splarrays[i], 5, axis=1)
		#print(hsparrays)
		for j in range(5):
			np.save(IMG_DIR+"/"+NPY_NAME_SPLIT.format(key1, key2, key3, count), hsparrays[j])
			pil_im = Image.fromarray(np.uint8(hsparrays[j]))
			pil_im.save(IMG_DIR+"/"+IMG_NAME_SPLIT.format(key1, key2, key3, count), 'PNG', quality=100, optimize=True)
			count = count + 1
