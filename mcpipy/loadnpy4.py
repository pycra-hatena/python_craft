# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import numpy as np
import pycra.npydata as nd
import pycra.wood as wood
import random
import sys
from time import sleep

NPY_2ND_FILE = "npydata-{0:04d}-{1:02d}.npy"
NPY_3RD_FILE = "npydata-{0:04d}-{1:02d}-{2:02d}.npy"
L03B_2ND_FILE = "npyl03-b-{0:04d}-{1:02d}.npy"
L03B_3RD_FILE = "npyl03-b-{0:04d}-{1:02d}-{2:02d}.npy"

if len(sys.argv) < 3:
    sys.exit("Usage: loadnpy4.py mesh1 mesh2 [mesh3]")

mc = minecraft.Minecraft()

mesh1 = int(sys.argv[1])
mesh2 = int(sys.argv[2])
mesh3 = None
if len(sys.argv) >= 4:
    mesh3 = int(sys.argv[3])

if mesh3 is None:
    sys.exit("No implement !")

h_array = np.load(nd.NPY_DIR+"/"+NPY_3RD_FILE.format(mesh1, mesh2, mesh3))
l_array = np.load(nd.NPY_DIR+"/"+L03B_3RD_FILE.format(mesh1, mesh2, mesh3))

for z in range(150):
    for x in range(225):
        r = random.random()
        hval = h_array[z][x]
        lval = l_array[z][x]
        hval *= 0.2
        mc.setBlocks(x, hval-1, z, x, hval-7, z, block.DIRT)
        if lval == 100:  # 田
            mc.setBlock(x, hval, z, block.GRASS)
            if r < 0.1:
                mc.setBlock(x, hval+1, z, block.FERN)
            #mc.setBlock(x, hval, z, block.FARMLAND)
            #mc.setBlock(x, hval+1, z, block.WHEAT)
        elif lval == 200: # その他農地
            mc.setBlock(x, hval, z, block.GRASS)
            if r < 0.1:
                mc.setBlock(x, hval+1, z, block.FERN)
            #mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_ORANGE)
        elif lval == 500: # 森林
            mc.setBlock(x, hval, z, block.GRASS)
            if r < 0.03:
                wood.wood(mc, x, hval+1, z)
            elif r < 0.1:
                mc.setBlock(x, hval+1, z, block.FERN)
        elif lval == 600: # 荒地
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_YELLOW)
        elif lval == 700: # 建物
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_RED)
        elif lval == 901: # 道路
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_LIGHT_GRAY)
        elif lval == 902: # 鉄道
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_GRAY)
        elif lval == 1000: # その他用地
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_PINK)
        elif lval == 1100: # 河川及び湖沼
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_BLUE)
        elif lval == 1400: # 海浜
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_CYAN)
        elif lval == 1500: # 海水域
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_PURPLE)
        elif lval == 1600: # ゴルフ場
            mc.setBlock(x, hval, z, block.HARDENED_CLAY_STAINED_LIME)
        else:
            mc.setBlock(x, hval, z, block.DIRT)
    sleep(0.02)
