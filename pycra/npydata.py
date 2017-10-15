# coding: utf-8

NPY_DIR = "/Users/pycra/Desktop/NPY_DATA"
NPY_DATA_REGEXP = 'npy(data|_5x5|lake)\-([0-9]+)\-([0-9]+)\-?([0-9]+)?\-?([0-9]+)?\-?(.+)?\.npy' # group(0~6)
NPY_FILENAME_REGEXP = '(.+)\.npy'

SURF_UNKNOWN = -1        # 不明
SURF_NO_DATA = 0         # "データなし"
SURF_OTHERWISE = 1       # "その他"
SURF_SEA_LEVEL = 2       # "海水面"
SURF_INLAND_WATER = 3    # "内水面"
SURF_SURFACE_LAYER = 4   # "表層面"
SURF_EARTH_SURFACE = 5   # "地表面"
