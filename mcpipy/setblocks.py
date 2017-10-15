# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

FORMAT = "setBlocks({0:d}, {1:d}, {2:d}, {3:d}, {4:d}, {5:d}, {6:d})"

mc = minecraft.Minecraft()

if len(sys.argv) < 5:
	sys.exit("Usage: setblocks.py [x1 y1 z1 x2 y2 z2 b]")

pos1_x = int(sys.argv[1])
pos1_y = int(sys.argv[2])
pos1_z = int(sys.argv[3])
pos2_x = int(sys.argv[4])
pos2_y = int(sys.argv[5])
pos2_z = int(sys.argv[6])
block_id = int(sys.argv[7])

mc.setBlocks(pos1_x, pos1_y, pos1_z, pos2_x, pos2_y, pos2_z, block_id)

mc.postToChat(FORMAT.format(pos1_x, pos1_y, pos1_z, pos2_x, pos2_y, pos2_z, block_id))
