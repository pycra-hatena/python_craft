# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

if len(sys.argv) < 4:
    sys.exit("Usage: tcp.py x y z")

x = int(sys.argv[1])
y = int(sys.argv[2])
z = int(sys.argv[3])

mc = minecraft.Minecraft()

mc.setBlocks(x-1, y, z-1, x+1, y+3, z+2, block.GLASS)
mc.setBlocks(x, y+1, z, x, y+2, z, block.AIR)
mc.setBlock(x, y+1, z+1, block.GLASS)
mc.setBlock(x, y+2, z+1, block.TORCH)
mc.player.setPos(x+0.5, y+1.0, z+0.5)
