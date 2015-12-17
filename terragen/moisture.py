import random
import numpy as np

from terragen.utils import log
from terragen.utils import find_neighbors
from terragen.terrain import make_groundwater

def closest_around(x, n, d=1):
    """ A faster neighborhood lookup function that ignores wrapping for speed """
    return x[n[0]-d:n[0]+d+1,n[1]-d:n[1]+d+1]

def make_moisture(world):
    """ Make moisture around rivers, and random groundwater locations """

    moisture_map = np.zeros(world['heightmap'].shape)

    x_, y_ = moisture_map.shape
    for x in xrange(x_):
        for y in xrange(y_):
            if world['river_grid'][x, y]:
                around = closest_around(moisture_map, (x, y), 30)
                around += 0.01

                around = closest_around(moisture_map, (x, y), 10)
                around += 0.05

    moisture_map = moisture_map.astype(int)

    groundwater = make_groundwater(world)
    return np.add(moisture_map, groundwater)
