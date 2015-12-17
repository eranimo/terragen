import numpy as np
import random
from terragen.terrain import make_terrain
from terragen.utils import Timer, log, elevation_at_percent_surface, latitude_ratio, randomize_color
from terragen.constants import TERRAIN, TEMPERATURE, BIOMES
from terragen.draw import draw_image
from terragen.rivers3 import make_rivers
from terragen.features import make_features
from terragen.moisture import make_moisture
#from terragen.biomes import decide_biomes

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
        heightmap, feature_image = make_features(heightmap, SIZE)
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
    world['sea_level_percent'] = sea_level_percent
    world['sea_level'] = elevation_at_percent_surface(world, sea_level_percent)

    log('Sea level: %i%% @ %i' % (sea_level_percent, world['sea_level']))

    heightmap, feature_image = make_features(heightmap, SIZE)

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

    with Timer('Making feature image'):

        def feature_image_func(cell):
            return cell

        def feature_image_color_func(value, x, y):
            if heightmap[x, y] < world['sea_level']:
                return (0, 0, 255)
            if value:
                return (255, 0, 0)
            return (100, 100, 100)

        draw_image(feature_image, feature_image_func, feature_image_color_func, 'features', SIZE)

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
    world['temperature_map'] = temperature_map
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
        world['river_grid'] = river_grid

    with Timer('Drawing rivers'):
        def get_river_grid_cell_func(cell):
            return cell

        def river_color_func(value, x, y):
            if world['heightmap'][x, y] < world['sea_level']:
                return (100, 100, 100)
            if value == 1: # rivers
                return 0, 0, 255
            if value == 2: # lakes
                return 255, 0, 255
            return 0, 255, 0

        draw_image(river_grid, get_river_grid_cell_func, river_color_func, 'rivers', SIZE)

    with Timer('Making moisture'):
        moisture_map = make_moisture(world)
        world['moisture_map'] = moisture_map
        moisture_min = np.min(moisture_map)
        moisture_max = np.max(moisture_map)
        moisture_avg = np.average(moisture_map)
        log("Min moisture: %i\n"
            "Max moisture: %i\n"
            "Avg moisture: %i" % (moisture_min, moisture_max, moisture_avg))

    with Timer('Drawing moisture'):
        def moisture_map_func(cell):
            return cell

        def moisture_map_color_func(value, x, y):
            if world['heightmap'][x, y] < world['sea_level']:
                return (0, 0, 255)
            if value == 0:
                return (0, 0, 0)
            return 100 + value, 100 + value, 100 + value

        draw_image(moisture_map, moisture_map_func, moisture_map_color_func, 'moisture', SIZE)

    # with Timer('Making biomes'):
    #     biome_map = decide_biomes(world)
    #     world['biome_map'] = biome_map
    #
    # with Timer('Drawing biomes'):
    #     def biome_map_func(cell):
    #         return cell
    #
    #     def biome_map_color_func(value, x, y):
    #         if world['heightmap'][x, y] < world['sea_level']:
    #             return (0, 0, 255)
    #         return BIOMES[value][2]
    #
    #     draw_image(biome_map, biome_map_func, biome_map_color_func, 'biomes', SIZE)
