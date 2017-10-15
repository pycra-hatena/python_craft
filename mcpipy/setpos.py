# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

FORMAT = "player.setPos({0:f}, {1:f}, {2:f})"

mc = minecraft.Minecraft()

if len(sys.argv) < 4:
	sys.exit("Usage: setpos.py [x y z]")

pos_x = float(sys.argv[1])
pos_y = float(sys.argv[2])
pos_z = float(sys.argv[3])

mc.player.setPos(pos_x, pos_y, pos_z)

mc.postToChat(FORMAT.format(pos_x, pos_y, pos_z))
