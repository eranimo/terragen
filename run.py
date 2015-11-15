import numpy as np
from terragen.terrain import make_terrain
from terragen.utils import Timer, log
from terragen.constants import TERRAIN
from terragen.draw import draw_image
from PIL import Image

if __name__ == "__main__":

    SIZE = 2**10 + 1

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

    min_height = np.min(heightmap)
    max_height = np.max(heightmap)
    avg_height = np.average(heightmap)
    log("Min height: %i\n"
          "Max height: %i\n"
          "Avg height: %i" % (min_height, max_height, avg_height))

    # decide the sea level
    sea_level = avg_height + 10

    # TERRAIN IMAGE
    with Timer('Making terrain image'):

        def delta_sea_level_func(cell):
            if cell < sea_level:
                return -(100 - (cell / sea_level) * 100)
            else:
                return ((cell - sea_level) / (max_height - sea_level)) * 100

        def terrain_color_func(value):
            for min_value, color in TERRAIN:
                if value <= min_value:
                    return color
            return color

        draw_image(heightmap, delta_sea_level_func, terrain_color_func, 'terrain', SIZE)
