import numpy as np
from random import randint
from terragen.utils import log, find_neighbors, cell_north, cell_east, cell_west, cell_south


def make_rivers(world):
    """ Make rivers """
    # a 2D array of values at each pixel representing the amount of water that has flowed through
    # this pixel into a neighbor
    rainflow = np.zeros(world['heightmap'].shape, dtype=int)

    # a working array that represents the rain flow after a certain number of calls to flow()
    waterlevel = np.zeros(world['heightmap'].shape, dtype=int)

    # an array of (x, y) coordinates of the nearest lowest neighbor
    lowest_neighbors = np.empty(world['heightmap'].shape, dtype='int, int')

    x_, y_ = rainflow.shape
    for x in xrange(x_):
        for y in xrange(y_):
            altitude = world['heightmap'][x, y]
            if altitude > world['sea_level']:
                rainflow[x, y] = 1
                waterlevel[x, y] = 1
                their_altitude, t_x, t_y = find_neighbors(world['heightmap'], (x, y), sort=True)[0]
                if their_altitude < world['heightmap'][x, y]:
                    lowest_neighbors[x, y] = (t_x, t_y)

    print(lowest_neighbors[10, 10])

    def flow():
        x_, y_ = rainflow.shape
        for x in xrange(x_):
            for y in xrange(y_):
                if waterlevel[x, y] != 0: # land pixels
                    # get the lowest neighbor
                    n = lowest_neighbors[x, y]

                    # is the lowest neighbor less than me?
                    if n:
                        # move my water to the neighbor
                        waterlevel[n[0], n[1]] += waterlevel[x, y]
                        # rainflow[n[0], n[1]] += waterlevel[x, y]
                        waterlevel[x, y] = 0

    for i in xrange(3):
        print('Flow %i' % i)
        flow()

    return waterlevel
