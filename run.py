import numpy as np
import random
from terragen.terrain import make_terrain
from terragen.utils import Timer, log, elevation_at_percent_surface, latitude_ratio, randomize_color
from terragen.constants import TERRAIN, TEMPERATURE
from terragen.draw import draw_image
from terragen.rivers4 import make_rivers
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

    log('Sea level: %i%% @ %i' % (sea_level_percent, world['sea_level']))


    # TERRAIN IMAGE
    with Timer('Making terrain image'):

        def delta_sea_level_func(cell):
            if cell < world['sea_level']:
                return -(100 - (cell / world['sea_level']) * 100)
            else:
                return ((cell - world['sea_level']) / (world['max_height'] - world['sea_level'])) * 100

        def terrain_color_func(value, x, y):
            for min_value, color in reversed(TERRAIN):
                if value > min_value:
                    return randomize_color(color, dist=3)
            return randomize_color(color, dist=3)

        draw_image(heightmap, delta_sea_level_func, terrain_color_func, 'terrain', SIZE)

    with Timer('Making land / water image'):

        def delta_sea_level_func(cell):
            if cell < world['sea_level']:
                return -1
            else:
                return 1

        def terrain_color_func(value, x, y):
            if value > 0:
                return (0, 255, 0)
            return (0, 0, 255)

        draw_image(heightmap, delta_sea_level_func, terrain_color_func, 'land_water', SIZE)

    log('Making temperatures')
    temperature_map = np.zeros(heightmap.shape)
    x_, y_ = heightmap.shape
    for x in xrange(x_):
        for y in xrange(y_):
            ratio = latitude_ratio(SIZE, y)
            avg_temp = 14.0
            volitility = round(abs(23))
            base_temp = -19.50
            min_temp = max(avg_temp - volitility, base_temp)
            # global avg temperature should be around ratio 0.4 and 0.6

            # part1 includes latitude only
            part1 = (abs(min_temp) + (avg_temp + volitility)) * ratio + min_temp
            # part2 includes latitude
            part2 = abs(heightmap[x, y] - world['sea_level']) / 6
            temperature_map[x, y] = round(part1, 2) - round(part2, 2)

    with Timer('Making temperature map'):

        def temp_get_func(cell):
            return cell

        def terrain_color_func(temperature, x, y):
            last_temp = -300
            for index, value in enumerate(TEMPERATURE):
                d_temp, color = value
                if last_temp <= temperature <= d_temp:
                    return color
                last_temp = d_temp
            return TEMPERATURE[-1][1]

        draw_image(temperature_map, temp_get_func, terrain_color_func, 'temp', SIZE)

    with Timer('Making rivers'):
        river_grid = make_rivers(world)

    with Timer('Drawing rivers'):
        def limit(v):
            if v > 255:
                return 255
            if v < 0:
                return 0
            return v

        def get_river_grid_cell_func(cell):
            return cell

        def river_color_func(value, x, y):
            if world['heightmap'][x, y] < world['sea_level']:
                return (100, 100, 100)
            if value:
                return 0, 0, 255
            return 0, 255, 0

        draw_image(river_grid, get_river_grid_cell_func, river_color_func, 'rivers', SIZE)
