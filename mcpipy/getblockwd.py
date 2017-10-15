# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

FORMAT = "getBlockWithData({0:d}, {1:d}, {2:d})=({3:d}, {4:d})"

mc = minecraft.Minecraft()

if len(sys.argv) < 4:
	sys.exit("Usage: getblockwd.py [x y z]")

pos_x = int(sys.argv[1])
pos_y = int(sys.argv[2])
pos_z = int(sys.argv[3])

block = mc.getBlockWithData(pos_x, pos_y, pos_z)

mc.postToChat(FORMAT.format(pos_x, pos_y, pos_z, block.id, block.data))
