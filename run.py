import os
import numpy as np
import random
from PIL import ImageFilter, Image
from terragen.terrain import make_terrain
from terragen.utils import Timer, log, elevation_at_percent_surface, latitude_ratio, randomize_color
from terragen.constants import TERRAIN, TEMPERATURE, BIOMES, RIVER_COLOR
from terragen.draw import draw_image
from terragen.rivers import make_rivers
from terragen.features import make_features
from terragen.moisture import make_moisture
from terragen.biomes import decide_biome

from scipy.ndimage.filters import gaussian_filter

class BlurFilter(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2):
        self.radius = radius

    def filter(self, image):
        return image.gaussian_blur(self.radius)

def count_folders(path):
    count = 1
    for f in os.listdir(path):
        if not os.path.isfile(os.path.join(path, f)):
            count += 1
    return count

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":

    SIZE = 2**9 + 1


    img = Image.new( 'RGB', (SIZE, SIZE), "black") # create a new black image
    terrain_image = img.load() # create the pixel map

    ensure_dir('images')
    folder_number = str(count_folders('./images'))
    folder = 'images/'+folder_number
    ensure_dir(folder)

    with Timer('Generating terrain'):
        # this function is expected to take ~30 seconds to run on the
        # following sizes:
        # 513 = 2-4 seconds
        # 1025 = 8-9 seconds
        # 2049 = 35-40 seconds
        heightmap = make_terrain(terrain_image, size=SIZE)
        heightmap, feature_image = make_features(heightmap, SIZE)
        img.save(folder+'/heightmap.png')

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

        draw_image(heightmap, delta_sea_level_func, terrain_color_func, 'terrain', SIZE, folder_number)

    with Timer('Making feature image'):

        def feature_image_func(cell):
            return cell

        def feature_image_color_func(value, x, y):
            if heightmap[x, y] < world['sea_level']:
                return (0, 0, 255)
            if value:
                return (255, 0, 0)
            return (100, 100, 100)

        draw_image(feature_image, feature_image_func, feature_image_color_func, 'features', SIZE, folder_number)

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

        draw_image(heightmap, delta_sea_level_func, terrain_color_func, 'land_water', SIZE, folder_number)

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
        def terrain_color_func(temperature, x, y):
            last_temp = -300
            for index, value in enumerate(TEMPERATURE):
                d_temp, color = value
                if last_temp <= temperature <= d_temp:
                    return color
                last_temp = d_temp
            return TEMPERATURE[-1][1]

        draw_image(temperature_map, None, terrain_color_func, 'temp', SIZE, folder_number)

    with Timer('Making rivers'):
        river_grid = make_rivers(world)
        world['river_grid'] = river_grid

    with Timer('Drawing rivers'):
        def river_color_func(value, x, y):
            if world['heightmap'][x, y] < world['sea_level']:
                return (100, 100, 100)
            if value == 1: # rivers
                return 0, 0, 255
            if value == 2: # lakes
                return 255, 0, 255
            return 0, 255, 0

        draw_image(river_grid, None, river_color_func, 'rivers', SIZE, folder_number)

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
        def moisture_map_color_func(value, x, y):
            if world['heightmap'][x, y] < world['sea_level']:
                return (0, 0, 255)
            if value == 0:
                return (0, 0, 0)
            return 100 + value, 100 + value, 100 + value

        draw_image(moisture_map, None, moisture_map_color_func, 'moisture', SIZE, folder_number)

    with Timer('Making biomes'):
        biome_map = decide_biome(world)
        world['biome_map'] = biome_map

    with Timer('Drawing biomes'):
        def biome_map_color_func(value, x, y):
            if world['heightmap'][x, y] < world['sea_level']:
                return (0, 0, 255)
            return BIOMES[value][2]

        draw_image(biome_map, None, biome_map_color_func, 'biomes', SIZE, folder_number)

    with Timer('Making realistic colored terrain'):
        img = Image.new( 'RGB', (SIZE, SIZE), "black")
        biome_map_real = img.load()
        x_, y_ = heightmap.shape
        for x in xrange(x_):
            for y in xrange(y_):
                if world['heightmap'][x, y] < world['sea_level']:
                    h_diff = int((world['sea_level'] - world['heightmap'][x, y]) / 2)
                    biome_map_real[x, y] = (RIVER_COLOR[0] - h_diff,
                                            RIVER_COLOR[1] - h_diff,
                                            RIVER_COLOR[2] - h_diff)
                elif world['river_grid'][x, y]:
                    biome_map_real[x, y] = RIVER_COLOR
                else:
                    b_real = BIOMES[biome_map[x, y]][3]
                    h_diff = (world['heightmap'][x, y] - world['sea_level']) / (world['max_height'] - world['sea_level'])
                    biome_map_real[x, y] = randomize_color((b_real[0] + int(b_real[0] * h_diff),
                                                            b_real[1] + int(b_real[1] * h_diff),
                                                            b_real[2] + int(b_real[2] * h_diff)))
        img.save(folder+'/satellite.png')
