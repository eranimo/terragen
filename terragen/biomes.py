import numpy as np

from terragen.utils import log
from terragen.constants import BIOMES

def decide_biome(world):
    """ Make moisture around rivers, and random groundwater locations """

    biome_map = np.zeros(world['heightmap'].shape, dtype=int)

    x_, y_ = biome_map.shape
    for x in xrange(x_):
        for y in xrange(y_):
            if world['heightmap'][x, y] >= world['sea_level']:
                temp = world['temperature_map'][x, y]
                rain = world['moisture_map'][x, y]
                if temp <= -10:
                    biome_map[x, y] = BIOMES[0][0]
                elif 5 < rain and temp <= 0:
                    biome_map[x, y] = BIOMES[2][0]
                elif 0 <= rain <= 5 and temp <= 0:
                    biome_map[x, y] = BIOMES[1][0]
                elif 5 < rain and 0 < temp <= 7:
                    biome_map[x, y] = BIOMES[7][0]
                elif 0 <= rain <= 2.5 and 0 < temp <= 20:
                    biome_map[x, y] = BIOMES[6][0]
                elif 2.5 < rain <= 5 and 0 < temp <= 20:
                    biome_map[x, y] = BIOMES[4][0]
                elif 0 <= rain <= 5 and 20 < temp:
                    biome_map[x, y] = BIOMES[3][0]
                elif 5 < rain <= 10 and 7 < temp <= 20:
                    biome_map[x, y] = BIOMES[5][0]
                elif 10 < rain <= 20 and 7 < temp <= 20:
                    biome_map[x, y] = BIOMES[8][0]
                elif 20 < rain and 7 < temp <= 20:
                    biome_map[x, y] = BIOMES[9][0]
                elif 5 < rain <= 20 and 20 < temp:
                    biome_map[x, y] = BIOMES[10][0]
                elif 20 < rain and 20 < temp:
                    biome_map[x, y] = BIOMES[11][0]

    return biome_map
