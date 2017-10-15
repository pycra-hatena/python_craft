# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import numpy as np
import pycra.npydata as nd
import sys
from time import sleep

LOG_FMT = "Z step ({}/{})"

# ここからスタート

mc = minecraft.Minecraft()

if len(sys.argv) < 3:
    print("loadnpy3.py npyfilename watersurface")
    exit(-1)

array = np.load(nd.NPY_DIR+"/"+sys.argv[1])
lksurf = np.load(nd.NPY_DIR+"/"+sys.argv[2])

mc.postToChat("Loadnpy3.py Start!")

(zshape, xshape) = array.shape

for z in range(zshape):
    for x in range(xshape):
        ls = lksurf[z][x]
        hval = array[z][x]
        if ls > hval:
            mc.setBlocks(x, hval, z, x, hval-7, z, block.DIRT)
            #mc.setBlocks(x, ls, z, x, hval+1, z, block.WATER)
        else:
            mc.setBlocks(x, hval-1, z, x, hval-7, z, block.DIRT)
            mc.setBlock(x, hval, z, block.GRASS)
        #sleep(0.01)
    mc.postToChat(LOG_FMT.format(z, zshape))
    sleep(0.1)

mc.postToChat("Loadnpy3.py Water start!")

for z in range(zshape):
    for x in range(xshape):
        ls = lksurf[z][x]
        hval = array[z][x]
        if ls > hval:
            #mc.setBlocks(x, hval, z, x, hval-7, z, block.DIRT)
            mc.setBlocks(x, ls, z, x, hval+1, z, block.WATER)
        #sleep(0.01)
    mc.postToChat(LOG_FMT.format(z, zshape))
    sleep(0.1)

mc.postToChat("Loadnpy3.py Finish!!!")
