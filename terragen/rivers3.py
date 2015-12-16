import random
import numpy as np

from terragen.utils import find_neighbors

def r_change(i=1):
    return random.randint(-i, i)

def make_rivers(world):
    num_rivers = random.randint(60, 120)

    I = np.nonzero(world['heightmap'] == world['sea_level'])
    coastline = list(zip(*I))
    np.random.shuffle(coastline)
    coastline = coastline[:num_rivers]

    print('Num rivers', num_rivers)

    river_grid = np.zeros(world['heightmap'].shape, dtype=bool)

    def uphill(size, x, y):
        altitude = world['heightmap'][x, y]
        nearby = find_neighbors(world['heightmap'], (x, y), sort=True)
        nearby = [i for i in nearby if i[0] > altitude]
        nearby = [i for i in nearby if not river_grid[i[1], i[2]]]

        if size > 800:
            return

        river_grid[x, y] = True
        if not nearby:
            # downhill(size + 1, x, y)
            return
        else:
            uphill(size + 1, nearby[0][1], nearby[0][2])

    # def downhill(size, x, y):
    #     altitude = world['heightmap'][x, y]
    #     nearby = find_neighbors(world['heightmap'], (x, y), sort=True)
    #     nearby = [i for i in nearby if i[0] < altitude]
    #     nearby = [i for i in nearby if not river_grid[i[1], i[2]]]
    #
    #     if size > 800:
    #         return
    #
    #     river_grid[x, y] = True
    #     if not nearby:
    #         uphill(size + 1, x, y)
    #     else:
    #         downhill(size + 1, nearby[0][1], nearby[0][2])


    for x, y in coastline:
        uphill(0, x, y)


    return river_grid
