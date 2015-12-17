import numpy as np

from terragen.utils import log
from terragen.constants import BIOMES

def decide_biome(world):
    """ Make moisture around rivers, and random groundwater locations """

    biome_map = np.zeros(world['heightmap'].shape)

    x_, y_ = biome_map.shape
    for x in xrange(x_):
        for y in xrange(y_):
            if world['heightmap'][x, y] >= world['sea_level']:
                temperature = world['temperature_map'][x, y]
                moisture = world['moisture_map'][x, y]
                if temperature < 0 and moisture < 100:
                    return 0
                elif 

    return biome_map
