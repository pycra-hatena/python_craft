# coding: utf-8

import mcpi.minecraft as minecraft
import mcpi.block as block

def dirobj(mc, x, y, z):
    gy = y+12
    # Green Arrow
    mc.setBlocks(x, gy, z, x, gy+11, z, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x-1, gy+10, z, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x+1, gy+10, z, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x, gy+10, z-1, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x, gy+10, z+1, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x-2, gy+9, z, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x+2, gy+9, z, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x, gy+9, z-2, block.HARDENED_CLAY_STAINED_GREEN)
    mc.setBlock(x, gy+9, z+2, block.HARDENED_CLAY_STAINED_GREEN)
    cy = gy+5
    # Red Arrow
    mc.setBlocks(x-5, cy, z, x+6, cy, z, block.HARDENED_CLAY_STAINED_RED)
    mc.setBlock(x+5, cy+1, z, block.HARDENED_CLAY_STAINED_RED)
    mc.setBlock(x+5, cy-1, z, block.HARDENED_CLAY_STAINED_RED)
    mc.setBlock(x+4, cy+2, z, block.HARDENED_CLAY_STAINED_RED)
    mc.setBlock(x+4, cy-2, z, block.HARDENED_CLAY_STAINED_RED)
    # Blue Arrow
    mc.setBlocks(x, cy, z-5, x, cy, z+6, block.HARDENED_CLAY_STAINED_BLUE)
    mc.setBlock(x, cy+1, z+5, block.HARDENED_CLAY_STAINED_BLUE)
    mc.setBlock(x, cy-1, z+5, block.HARDENED_CLAY_STAINED_BLUE)
    mc.setBlock(x, cy+2, z+4, block.HARDENED_CLAY_STAINED_BLUE)
    mc.setBlock(x, cy-2, z+4, block.HARDENED_CLAY_STAINED_BLUE)
    # Pillar
    mc.setBlocks(x, y, z, x, gy-1, z, block.HARDENED_CLAY_STAINED_WHITE)
    # Torch
    mc.setBlock(x, gy+12, z, block.TORCH)
    mc.setBlock(x-3, gy+9, z, block.TORCH.id, 2)
    mc.setBlock(x+3, gy+9, z, block.TORCH.id, 1)
    mc.setBlock(x, gy+9, z-3, block.TORCH.id, 4)
    mc.setBlock(x, gy+9, z+3, block.TORCH.id, 3)
    mc.setBlock(x+7, cy, z, block.TORCH.id, 1)
    mc.setBlock(x+6, cy, z+1, block.TORCH.id, 3)
    mc.setBlock(x+6, cy, z-1, block.TORCH.id, 4)
    mc.setBlock(x, cy, z+7, block.TORCH.id, 3)
    mc.setBlock(x+1, cy, z+6, block.TORCH.id, 1)
    mc.setBlock(x-1, cy, z+6, block.TORCH.id, 2)
