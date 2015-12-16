import random
import time
import datetime
from colored import fore, style

import numpy as np

def log(string):
    string = string.replace('\n', '\n'.ljust(15, ' '))
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    print(('[' + fore.BLUE + '%s' + style.RESET + '] %s') %
          (current_time, string))

class Timer:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        print(('[' + fore.BLUE + '%s' + \
              style.RESET + '] %s ' + \
              style.BOLD + '%.03f'+style.RESET + \
              ' seconds') % (current_time, (self.name+':').ljust(80), self.interval))


def elevation_at_percent_surface(world, percent):
    return round(world['avg_height'] * (percent * 2 / 100))

def cell_north(array, x, y):
    size = len(array)
    if x == 0:
        return array[x, size - 1 - y], x, size - 1 - y
    return array[x - 1, y], x - 1, y

def cell_south(array, x, y):
    size = len(array)
    if x == size-1:
        return array[x, size - 1 - y], x, size - 1 - y
    return array[x+1, y], x + 1, y

def cell_west(array, x, y):
    size = len(array)
    if y == 0:
        return array[x, size-1], x, size - 1
    return array[x, y-1], x, y - 1

def cell_east(array, x, y):
    size = len(array)
    if y == size-1:
        return array[x, 0], x, 0
    return array[x, y+1], x, y + 1

def cell_north_west(array, x, y):
    size = len(array)
    if x == 0:
        if y == 0:
            return array[x, y], x, y
        else:
            return array[x, size - 1 - y + 1], x, size - 1 - y + 1
    return array[x-1, y-1], x - 1, y - 1

def cell_north_east(array, x, y):
    size = len(array)
    if x == 0:
        if y == 0:
            return array[x, size - 2], x, size - 2
        else:
            return array[x, size - 1 - y - 1], x, size - 1 - y - 1
    if y == size-1:
        return array[x-1, 0], x - 1, 0
    else:
        return array[x-1, y+1], x - 1, y + 1

def cell_south_west(array, x, y):
    size = len(array)
    if x == size-1:
        if y == 0:
            return array[x, 0], x, 0
        else:
            return array[x, size - 1 - y + 1], x, size - 1 - y + 1
    return array[x+1, y-1], x + 1, y - 1

def cell_south_east(array, x, y):
    size = len(array)
    if x == size-1:
        if y == size-1:
            return array[size - 1, size - 1], size - 1, size - 1
        else:
            return array[x, size - 1 - y - 1], x, size - 1 - y - 1
    if y == size-1:
        return array[x+1, 0], x + 1, 0
    else:
        return array[x+1, y+1], x + 1, y + 1

def find_neighbors(array, location, radius=1, sort=False):
    """
    Return a list of (altitude, x, y) tuples representing neighboring cells.
    Follows wrapping rules for heightmap.
    Specify a radius to bubble outwards from the given coordinate.
    Sort will sort the list by elevation.
    """
    x, y = location
    def get_neighbors(n, x=x, y=y):
        return [
            cell_north(n, x, y),
            cell_south(n, x, y),
            cell_east(n, x, y),
            cell_west(n, x, y),
            cell_north_east(n, x, y),
            cell_north_west(n, x, y),
            cell_south_east(n, x, y),
            cell_south_west(n, x, y),
        ]
    neighbors = get_neighbors(array)

    if radius > 1:
        for n in neighbors:
            neighbors = neighbors + get_neighbors(array, x=n[1], y=n[2])
        # remove duplicates
        neighbors = list(set(neighbors))
    if sort:
        neighbors.sort(key=lambda i: i[0])
    return neighbors

def latitude_ratio(size, x):
    ratio = float(x) / float(size)
    if ratio < 0.5:
        ratio /= 0.5
    else:
        ratio = (1 - ratio) / 0.5
    return ratio

def limit(value):
    if value > 255:
        return 255
    if value < 0:
        return 0
    return value

def randomize_color(color, dist=1):
    colors = [
        color,
        (limit(color[0] - dist), limit(color[1] - dist), limit(color[2] - dist)),
        (limit(color[0] + dist), limit(color[1] + dist), limit(color[2] + dist)),
        (limit(color[0] - dist), limit(color[1] + dist), limit(color[2] - dist)),
        (limit(color[0] + dist), limit(color[1] - dist), limit(color[2] - dist)),
        (limit(color[0] - dist), limit(color[1] + dist), limit(color[2] - dist)),
        (limit(color[0] - dist), limit(color[1] - dist), limit(color[2] + dist)),
        (limit(color[0] + dist), limit(color[1] - dist), limit(color[2] + dist)),
        (limit(color[0] - dist), limit(color[1] + dist), limit(color[2] - dist))
    ]
    return random.choice(colors)
