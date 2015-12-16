from random import randint
import numpy as np

from terragen.utils import log, find_neighbors, cell_north, cell_east, cell_west, cell_south

def r_change(i=1):
    return random.randint(-i, i)

def make_rivers(world):
    mountain_cutoff = world['max_height'] - 50
    mountains = np.transpose(np.nonzero(world['heightmap'] >= mountain_cutoff))
    np.random.shuffle(mountains)

    log('%i mountains or %0.5f%%' %
        (len(mountains), (float(len(mountains)) / float(world['size']**2)) * 100))

    num_rivers = randint(0, int(len(mountains) * 0.10))
    log('Making %i rivers' % num_rivers)
    river_sources = mountains[:num_rivers]

    river_grid = np.zeros(world['heightmap'].shape, dtype=np.bool)
    water_level = np.copy(world['heightmap'])

    def make_lake(start_x, start_y, start_altitude):
        """
            start_x  : X coordinate of start of lake
            start_y  : Y coordinate of start of lake
            start_altitude : altitude of starting point
        """
        # make a lake here
        # the lake has a level, which is how deep the lake is at its deepest
        # perform flood fill for all neighboring pixels < altitude + level
        # raising the water level of each flooded cell to be the target altitude
        # returns the coordinates of the point where the lake spills over
        level = 1
        def step(x, y):
            this_altitude = world['heightmap'][x, y]
            log('\t\tFlood step %i, %i (%i)' % (x, y, this_altitude))
            water_level[x, y] = start_altitude + level

            if this_altitude + level > start_altitude:
                # if the this_altitude + level is greater than start_altitude
                log('\t\tFound a spill over at %i, %i (%i)' % (x, y, this_altitude))
                return x, y
            river_grid[x, y] = True

            # flood into neighbors
            # if any of their recursive chains finds a spill over,
            # return it immediately and celebrate
            north = cell_north(world['heightmap'], x, y)
            r_n = step(north[1], north[2])
            if r_n:
                return r_n

            south = cell_south(world['heightmap'], x, y)
            r_s = step(south[1], south[2])
            if r_s:
                return r_s

            east = cell_east(world['heightmap'], x, y)
            r_e = step(east[1], east[2])
            if r_e:
                return r_e

            west = cell_west(world['heightmap'], x, y)
            r_w = step(west[1], west[2])
            if r_w:
                return r_w

            return False

        # rise the level of the lake until you find a spill point
        rising = True
        while rising is True:
            log('\tLake level at %i' % level)
            found = step(start_x, start_y)
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

        if size > 800:
            return

        river_grid[x, y] = True
        if not nearby:
            # found a depression
            # make a lake here
            log('Flood fill at %i, %i (%i)' % (x, y, altitude))
            lake_exit = make_lake(x, y, altitude)
            log('Lake exit found at %i, %i' % lake_exit)
            if lake_exit[0] == x or lake_exit[1] == y:
                raise Exception("Lake algorithm didn't work")
            next_segment(size + 1, lake_exit[0], lake_exit[1])
        else:
            next_segment(size + 1, nearby[0][1], nearby[0][2])


    for x, y in river_sources:
        next_segment(0, x, y)


    return river_grid
