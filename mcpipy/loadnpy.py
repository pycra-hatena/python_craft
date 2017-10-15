# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import numpy as np
import sys
from time import sleep

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"
LOG_FMT = "Z step ({}/{})"

# ここからスタート

mc = minecraft.Minecraft()

if len(sys.argv) < 2:
    sys.exit("loadnpy.py npyfilename")

array = np.load(NPY_DIR+"/"+sys.argv[1])

mc.postToChat("Loadnpy.py Start!")

mc.setBlocks(-1, 4, -1, -1, 6, -1, block.AIR)
mc.setBlock(-1, 3, -1, block.STONE)
mc.player.setTilePos(-1, 4, -1)
sleep(1)

(zshape, xshape) = array.shape
ymin = array.min()
ymax = array.max()
if ymin > 0:
    ymin = 0
mc.setBlocks(0, ymin, 0, xshape-1, ymax, zshape-1, block.AIR)

sleep(0.1)

for z in range(zshape):
    for x in range(xshape):
        hval = array[z][x]
        if hval > 8:
            mc.setBlocks(x, hval-8, z, x, 0, z, block.STONE)
        mc.setBlocks(x, hval-1, z, x, hval-7, z, block.DIRT)
        mc.setBlock(x, hval, z, block.GRASS)
        #sleep(0.01)
    mc.postToChat(LOG_FMT.format(z, zshape))
    sleep(0.1)

mc.postToChat("Loadnpy.py Finish!!!")
