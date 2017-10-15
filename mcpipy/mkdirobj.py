# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import pycra.dirobj as dirobj

mc = minecraft.Minecraft()
mc.events.clearAll()

while True:
    blockHits = mc.events.pollBlockHits()
    if blockHits:
        blockHit = blockHits[0]
        if blockHit.face == 1:
            x = blockHit.pos.x
            y = blockHit.pos.y
            z = blockHit.pos.z
            blockId = mc.getBlock(x, y, z)
            while blockId != block.AIR:
                y = y + 1
                blockId = mc.getBlock(x, y, z)
            dirobj.dirobj(mc, x, y, z)
