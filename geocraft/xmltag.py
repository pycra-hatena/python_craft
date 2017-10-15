# coding: utf-8

import xml.etree.ElementTree as ET
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: xmltagdump.py xmlfilename (tag)")

tree = ET.parse(sys.argv[1])
root = tree.getroot()

if len(sys.argv) >= 3:
    for e in root.getiterator(sys.argv[2]):
        print(e.tag)
else:
    for e in root.getiterator():
        print(e.tag)
