# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plot
import pycra.npydata as nd
import sys

NPY_DATA = "npydata-5340-22.npy"
XML_RAILCL = "FG-GML-534022-ALL-20170401/FG-GML-534022-RailCL-20170401-0001.xml"
RCL_DATA = "npyrcl-5340-22.npy"

class World:
    """ class for World coordinate """
    def __init__(self, mesh1, mesh2, geo_array, rcl_array):
        self.mesh1 = mesh1
        self.mesh2 = mesh2
        self.geo_array = geo_array
        self.rcl_array = rcl_array
        self.origin1 = Position.convert_mesh1(mesh1)
        self.origin2 = Position.convert_mesh2(mesh1, mesh2)

    def convert_position(self, pos):
        offset = Position(pos.latitude - self.origin2.latitude, pos.longitude - self.origin2.longitude)
        index = Index(int(1499.0 * (1.0 - (offset.latitude / ((1.0/1.5)/8.0)))), int(2249.0 * offset.longitude / (1.0/8.0)))
        return index

class RailCL:
    """ class for Rail Center Line """
    def __init__(self, elem):
        e = elem.find("{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}vis")
        if e is None:
            raise Exception("{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}vis is not found")
        if e.text == "表示":
            self.vis = True
        else:
            self.vis = False
        e = elem.find("{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}loc/{http://www.opengis.net/gml/3.2}Curve/{http://www.opengis.net/gml/3.2}segments/{http://www.opengis.net/gml/3.2}LineStringSegment/{http://www.opengis.net/gml/3.2}posList")
        if e is None:
            raise Exception("{http://www.opengis.net/gml/3.2}posList is not found")
        self.array = text2array(e.text.strip())

class Position:
    """ class for Latitude, Longitude """
    @classmethod
    def convert_mesh1(self, mesh1):
        return Position(float(mesh1//100)/1.5, float(mesh1%100)+100.0)

    @classmethod
    def convert_mesh2(self, mesh1, mesh2):
        pos = Position(float(mesh1//100)/1.5, float(mesh1%100)+100.0)
        offset = Position((1.0/1.5)/8.0 * (mesh2//10), 1.0/8.0 * (mesh2%10))
        pos.add(offset)
        return pos

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def add(self, offset):
        self.latitude += offset.latitude
        self.longitude += offset.longitude

    def __str__(self):
        return "({0:f}, {1:f})".format(self.latitude, self.longitude)

class Index:
    """ class for Array index """
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __str__(self):
        return "({0:d}, {1:d})".format(self.y, self.x)

def text2array(text):
    lines = text.split()
    array = np.empty((len(lines)), dtype=np.float)
    i = 0
    for l in lines:
        array[i] = float(l)
        i += 1
    return array.reshape((len(lines)//2, 2))

geo_array = np.load(nd.NPY_DIR+"/"+NPY_DATA)

tree = ET.parse(XML_RAILCL)
root = tree.getroot()

rails = []

for e in root.getiterator("{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}RailCL"):
    rc = RailCL(e)
    rails.append(rc)

world = World(5340, 22, geo_array, rails)
print("World.origin1="+str(world.origin1))
print("World.origin2="+str(world.origin2))
(y_max, x_max) = world.geo_array.shape
print("World.geo_array.shape=({0}, {1})".format(y_max, x_max))

array = np.zeros(world.geo_array.shape)
for r in rails:
    (y_max, x_max) = r.array.shape
    for y in range(y_max):
        pos = Position(r.array[y][0], r.array[y][1])
        index = world.convert_position(pos)
        if r.vis:
            array[index.y][index.x] = 2
        else:
            array[index.y][index.x] = 1

plot.imshow(array, interpolation='nearest')
plot.colorbar()
plot.show()
