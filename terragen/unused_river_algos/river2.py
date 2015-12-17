import numpy as np
from random import randint
from terragen.utils import log, find_neighbors, cell_north, cell_east, cell_west, cell_south


def make_rivers(world):
    """ Make rivers """

    heightmap = world['heightmap']
    sea_level = world['sea_level']

    # a 2D array of values at each pixel representing the amount of water that has flowed through
    # this pixel into a neighbor
    rain_flow = np.zeros(world['heightmap'].shape, dtype=int)

    # a working array that represents the rain flow after a certain number of calls to flow()
    water_amount = np.zeros(world['heightmap'].shape, dtype=int)

    # an 2D array of 0 - 255 representing water level
    water_level = np.copy(world['heightmap'])

    # an array of (x, y) coordinates of the nearest lowest neighbor
    lowest_neighbors = np.zeros(world['heightmap'].shape, dtype='int, int, int')

    # a 2D array to make looking up land / water easier
    is_land = np.zeros(world['heightmap'].shape, dtype=int)

    # seed the map with initial rainfall
    # TODO: make this not uniform. Maybe perlin noise?
    x_, y_ = rain_flow.shape
    for x in xrange(x_):
        for y in xrange(y_):
            altitude = world['heightmap'][x, y]
            if altitude > sea_level:
                is_land[x, y] = 1
                rain_flow[x, y] = 1
                water_amount[x, y] = 1
                lowest_neighbors[x, y] = find_neighbors(water_level, (x, y), sort=True)[0]


    def flow(count=1):
        x_, y_ = rain_flow.shape
        for x in xrange(x_):
            for y in xrange(y_):
                if is_land[x, y] == 1:
                    # get the lowest neighbor
                    other_altitude, t_x, t_y = lowest_neighbors[x, y]

                    # if the lowest neighbor is higher than me,
                    # i'm in a depression. Raise the water level accordingly

                    if other_altitude >= water_level[x, y]:
                        # update the water level to the lowest neighbor
                        water_level[x, y] = other_altitude + 1

                    if is_land[t_x, t_y]:
                        water_amount[t_x, t_y] += water_amount[x, y]
                        rain_flow[t_x, t_y] += water_amount[x, y]
                    water_amount[x, y] = 0

    for i in xrange(100):
        flow(i)
        print(np.sum(water_amount))

    print(rain_flow)


    return rain_flow, water_level, water_amount
