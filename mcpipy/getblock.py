# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

FORMAT = "getBlock({0:d}, {1:d}, {2:d})={3:d}"

mc = minecraft.Minecraft()

if len(sys.argv) < 4:
	sys.exit("Usage: getblock.py [x y z]")

pos_x = int(sys.argv[1])
pos_y = int(sys.argv[2])
pos_z = int(sys.argv[3])

blockId = mc.getBlock(pos_x, pos_y, pos_z)

mc.postToChat(FORMAT.format(pos_x, pos_y, pos_z, blockId))
