# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import sys

FORMAT = "player.getPos()=({0:f}, {1:f}, {2:f})"

mc = minecraft.Minecraft()

if len(sys.argv) > 1:
	sys.exit("Usage: getpos.py")

pos = mc.player.getPos()

mc.postToChat(FORMAT.format(pos.x, pos.y, pos.z))
