# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import numpy as np
import sys
from time import sleep

NPY_DIR = "/Users/sakai/Desktop"
NPY_FILE = "npydata-{0:04d}-{1:02d}.npy"

mc = minecraft.Minecraft()
mc.postToChat("Loadnpy2.py Start!")

if len(sys.argv) < 3:
    print("loadnpy2.py mesh1 mesh2")
    exit(-1)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])

array = np.load(NPY_DIR+"/"+NPY_FILE.format(mesh1, mesh2))
(zshape, xshape) = array.shape

for z in range(zshape):
    sleep(0.01)
    for x in range(xshape):
        hval = array[z][x]
        mc.setBlocks(x, hval-1, z, x, hval-7, z, block.DIRT)
        mc.setBlock(x, hval, z, block.GRASS)
        sleep(0.001)

mc.postToChat("Loadnpy2.py Finish!!!")
