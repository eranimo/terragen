from random import randint
import numpy as np
# import sys
# sys.setrecursionlimit(10000)

from terragen.utils import log, find_neighbors, cell_north, cell_east, cell_west, cell_south, cell_random

def make_rivers(world):
    mountain_cutoff = world['sea_level'] + 40
    mountains = np.transpose(np.nonzero(world['heightmap'] >= mountain_cutoff))
    np.random.shuffle(mountains)

    log('%i mountains or %0.5f%%' %
        (len(mountains), (float(len(mountains)) / float(world['size']**2)) * 100))

    num_rivers = randint(0, int(len(mountains) * 0.10))
    log('Making %i rivers' % num_rivers)
    river_sources = mountains[:num_rivers]

    river_grid = np.zeros(world['heightmap'].shape)
    water_level = np.copy(world['heightmap'])

    def make_lake(start_x, start_y, start_altitude):
        """
            start_x  : X coordinate of start of lake
            start_y  : Y coordinate of start of lake
            start_altitude : altitude of starting point
        """
        # make a lake here
        # the lake has a level, which is how deep the lake is at its deepest
        # perform flood fill for all neighboring pixels < start_altitude + level
        # check all cells around the outside of the lake if any of them are lower than the pixels
        # inside the lake. IF one of them are, it's a spill and return it.
        # if there are none, then raise the level
        level = 1
        def step(x, y, last_altitude):
            this_altitude = world['heightmap'][x, y]
            log('\t\tFlood step %i, %i (%i)' % (x, y, this_altitude))

            if river_grid[x, y] == 2:
                # already checked this cell
                return False

            if this_altitude > start_altitude + level:
                return False

            # if this_altitude < last_altitude:
            #     # spill over here
            #     log('\t\tFound a spill over at %i, %i (%i)' % (x, y, this_altitude))
            #     return x, y

            # set this cell as a lake
            river_grid[x, y] = 2

            # flood into neighbors
            # if any of their recursive chains finds a spill over,
            # return it immediately and celebrate

            west = cell_north(world['heightmap'], x, y)
            r_w = step(west[1], west[2], this_altitude)
            if r_w:
                return r_w

            east = cell_north(world['heightmap'], x, y)
            r_w = step(east[1], east[2], this_altitude)
            if r_w:
                return r_w

            south = cell_north(world['heightmap'], x, y)
            r_w = step(south[1], south[2], this_altitude)
            if r_w:
                return r_w

            north = cell_north(world['heightmap'], x, y)
            r_w = step(north[1], north[2], this_altitude)
            if r_w:
                return r_w

            return False

        # rise the level of the lake until you find a spill point
        rising = True
        while rising is True:
            log('\tLake level at %i' % level)
            found = step(start_x, start_y, start_altitude)
            if found is not False:
                return found
            else:
                level += 1

    def next_segment(size, x, y):
        log('next_segment %i, %i' % (x, y))
        altitude = world['heightmap'][x, y]
        nearby = find_neighbors(world['heightmap'], (x, y), sort=True)
        nearby = [i for i in nearby if i[0] < altitude]
        nearby = [i for i in nearby if not river_grid[i[1], i[2]]]


        river_grid[x, y] = 1
        if not nearby:
            # found a depression
            # make a lake here
            log('Flood fill at %i, %i (%i)' % (x, y, altitude))
            lake_exit = make_lake(x, y, altitude)
            if lake_exit is None or lake_exit is False:
                return # give up
            if lake_exit[0] == x and lake_exit[1] == y:
                return
            log('Lake exit found at %i, %i' % lake_exit)
            next_segment(size + 1, lake_exit[0], lake_exit[1])
        else:
            next_segment(size + 1, nearby[0][1], nearby[0][2])


    for x, y in river_sources:
        if x >= 0 and y >= 0 and x < world['size'] and y < world['size']:
            log('Starting a river at %i, %i' % (x, y))
            next_segment(0, x, y)


    return river_grid
