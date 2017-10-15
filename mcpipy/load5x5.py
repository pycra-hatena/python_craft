# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import numpy as np
import sys
from time import sleep

NPY_DIR = "/Users/sakai/Desktop"
NPY5x5_FILE = "npydata-{0:04d}-{1:02d}-5x5.npy"
LOG_FMT = "z range ({} / {})"

mc = minecraft.Minecraft()
mc.postToChat("Load5x5.py Start!")

if len(sys.argv) < 3:
    print("load5x5.py mesh1 mesh2")
    exit(-1)

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])

array = np.load(NPY_DIR+"/"+NPY5x5_FILE.format(mesh1, mesh2))
(zshape, xshape) = array.shape

mc.setBlocks(0, 100, 0, xshape-1, -10, zshape-1, block.AIR)

for z in range(zshape):
    mc.postToChat(LOG_FMT.format(z, zshape-1))
    sleep(0.1)
    for x in range(xshape):
        hval = array[z][x]
        if hval > -1:
            mc.setBlocks(x, hval-1, z, x, hval-7, z, block.DIRT)
            mc.setBlock(x, hval, z, block.GRASS)
            if hval-7 > -10:
                mc.setBlocks(x, hval-7, z, x, -10, z, block.STONE)
            sleep(0.01)

mc.postToChat("Load5x5.py Finish!!!")
