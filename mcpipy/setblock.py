# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

FORMAT = "setBlock({0:d}, {1:d}, {2:d}, {3:d})"
FORMAT2 = "setBlock({0:d}, {1:d}, {2:d}, {3:d}, {4:d})"

mc = minecraft.Minecraft()

if len(sys.argv) < 5:
	sys.exit("Usage: setblock.py [x y z b d]")

pos_x = int(sys.argv[1])
pos_y = int(sys.argv[2])
pos_z = int(sys.argv[3])
block_id = int(sys.argv[4])
block_data = None
if len(sys.argv) >= 6:
	block_data = int(sys.argv[5])

if block_data is None:
	mc.setBlock(pos_x, pos_y, pos_z, block_id)
	mc.postToChat(FORMAT.format(pos_x, pos_y, pos_z, block_id))
else:
	mc.setBlock(pos_x, pos_y, pos_z, block_id, block_data)
	mc.postToChat(FORMAT2.format(pos_x, pos_y, pos_z, block_id, block_data))
