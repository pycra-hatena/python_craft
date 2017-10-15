# coding: utf-8

import numpy as np
import pycra.npydata as nd
import re
import sys

if len(sys.argv) < 3:
    sys.exit("Usage: npyscale.py npyfilename scale")

m = re.search(nd.NPY_FILENAME_REGEXP, sys.argv[1])
if m is None:
    sys.exit("Bad npyfilename.")

print(m.group(0))
print(m.group(1))

scale = float(sys.argv[2])

array = np.load(nd.NPY_DIR+"/"+sys.argv[1])

array = array * scale

np.save(nd.NPY_DIR+"/"+m.group(1)+"-scaled.npy", array)
