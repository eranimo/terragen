import numpy as np
import random
from terragen.terrain import make_terrain
from terragen.utils import Timer, log, elevation_at_percent_surface
from terragen.constants import TERRAIN
from terragen.draw import draw_image
from terragen.rivers import make_rivers
from PIL import Image

if __name__ == "__main__":

    SIZE = 2**9 + 1

    img = Image.new( 'RGB', (SIZE, SIZE), "black") # create a new black image
    terrain_image = img.load() # create the pixel map

    with Timer('Generating terrain'):
        # this function is expected to take ~30 seconds to run on the
        # following sizes:
        # 513 = 2-4 seconds
        # 1025 = 8-9 seconds
        # 2049 = 35-40 seconds
        heightmap = make_terrain(terrain_image, size=SIZE)
        img.save('images/heightmap.png')

    world = dict(size=SIZE,
                 heightmap=heightmap,
                 min_height=np.min(heightmap),
                 max_height=np.max(heightmap),
                 avg_height=np.average(heightmap))
    log("Min height: %i\n"
        "Max height: %i\n"
        "Avg height: %i" % (world['min_height'], world['max_height'], world['avg_height']))

    # decide the sea level
    sea_level_percent = random.randint(50, 70)
    world['sea_level'] = elevation_at_percent_surface(world, sea_level_percent)

    log('Sea level: %i%%' % (sea_level_percent))


    # TERRAIN IMAGE
    with Timer('Making terrain image'):

        def delta_sea_level_func(cell):
            if cell < world['sea_level']:
                return -(100 - (cell / world['sea_level']) * 100)
            else:
                return ((cell - world['sea_level']) / (world['max_height'] - world['sea_level'])) * 100

        def terrain_color_func(value, x, y):
            for min_value, color in TERRAIN:
                if value <= min_value:
                    return color
            return color

        draw_image(heightmap, delta_sea_level_func, terrain_color_func, 'terrain', SIZE)


    rivers, world = make_rivers(world)
    with Timer('Drawing rivers'):
        def delta_sea_level_func(cell):
            if cell < world['sea_level']:
                return -(100 - (cell / world['sea_level']) * 100)
            else:
                return ((cell - world['sea_level']) / (world['max_height'] - world['sea_level'])) * 100

        def terrain_color_func(value, x, y):
            if world['river_array'][x, y]:
                return (0, 0, 255)
            for min_value, color in TERRAIN:
                if value <= min_value:
                    return color
            return color

        draw_image(heightmap, delta_sea_level_func, terrain_color_func, 'rivers', SIZE)
    print(np.transpose(np.nonzero(world['river_array'])))
