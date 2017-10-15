# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block
import math
import random
import sys

# ここからスタート

mc = minecraft.Minecraft()

if len(sys.argv) < 6:
    sys.exit("Usage: leaves x y z radius density")

x = float(sys.argv[1])
y = float(sys.argv[2])
z = float(sys.argv[3])
r = float(sys.argv[4])
d = float(sys.argv[5])

min_x = int(x - r)
max_x = int(x + r)
min_y = int(y - r)
max_y = int(y + r)
min_z = int(z - r)
max_z = int(z + r)

for dy in range(min_y, max_y+1):
    for dx in range(min_x, max_x+1):
        for dz in range(min_z, max_z+1):
            xx =  dx - x
            yy =  dy - y
            zz =  dz - z
            s = xx * xx + yy * yy + zz * zz
            sq = math.sqrt(s)
            if sq <= r:
                block_id = mc.getBlock(dx, dy, dz)
                if block_id == block.AIR:
                    if sq < r - 0.5:
                        if random.random() < d:
                            mc.setBlock(dx, dy, dz, block.LEAVES)
                    else:
                        mc.setBlock(dx, dy, dz, block.LEAVES)
