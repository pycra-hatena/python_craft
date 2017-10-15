# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import math
import random
import sys

def leaves(mc, x, y, z, radius, density):
    min_x = int(x - radius)
    max_x = int(x + radius)
    min_y = int(y - radius)
    max_y = int(y + radius)
    min_z = int(z - radius)
    max_z = int(z + radius)
    for dy in range(min_y, max_y+1):
        for dx in range(min_x, max_x+1):
            for dz in range(min_z, max_z+1):
                xx =  dx - x
                yy =  dy - y
                zz =  dz - z
                s = xx * xx + yy * yy + zz * zz
                sq = math.sqrt(s)
                if sq <= radius:
                    block_id = mc.getBlock(dx, dy, dz)
                    if block_id == block.AIR:
                        if sq < radius - 0.5:
                            if random.random() < density:
                                mc.setBlock(dx, dy, dz, block.LEAVES)
                        else:
                            mc.setBlock(dx, dy, dz, block.LEAVES)

def wood(mc, x, y, z):
    height = 4 + int(random.random() * 5)
    mc.setBlocks(x, y, z, x, y + height, z, block.WOOD)
    offset = height * 0.25
    leaves(mc, x, y + height - offset, z, height * 0.5, 0.5)

if __name__ == '__main__':
    # ここからスタート
    mc = minecraft.Minecraft()

    if len(sys.argv) < 4:
        sys.exit("Usage: wood x y z")

    x = float(sys.argv[1])
    y = float(sys.argv[2])
    z = float(sys.argv[3])

    wood(mc, x, y, z)
