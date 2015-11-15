import numpy as np
from random import randint
from terragen.utils import log, neighbors


class RiverPart(object):
    def __init__(self, river):
        self.prev_segments = []
        self.next_segments = []
        self.river = river

    def next(self):
        """ Finds the next river segment """
        pass

class RiverSegment(RiverPart):
    def __init__(self, river, location):
        self.location = location
        river.world['river_array'][location[0], location[1]] = True
        super(RiverSegment, self).__init__(river)

class Lake(RiverPart):
    def __init__(self, river):
        self.parts = []
        super(Lake, self).__init__(river)

class River:
    def __init__(self, world, location):
        self.world = world
        self.source = RiverSegment(self, location) # river segment

    def flow(self):
        """ Iterate over the river, eroding and depositing sedements. """
        pass

def make_rivers(world):
    """
    Generate rivers. Returns a tuple containing:
    - River instances
    - new world dictionary, containging:
        - new heightmap after river erosion and deposition
        - river_array: numpy boolean array in shape of heightmap showing where rivers are
    """
    mountain_cutoff = world['max_height'] - 15
    mountains = np.transpose(np.nonzero(world['heightmap'] >= mountain_cutoff))
    np.random.shuffle(mountains)

    log('%i mountains or %0.5f%%' %
        (len(mountains), (float(len(mountains)) / float(world['size']**2)) * 100))

    num_rivers = 1 # randint(0, int(len(mountains) * 0.10))
    log('Making %i rivers' % num_rivers)
    river_sources = mountains[:num_rivers]

    # since rivers look the same on the images, this is a boolean array
    world['river_array'] = np.zeros(world['heightmap'].shape, dtype=np.bool)

    rivers = []
    for source in river_sources:
        river = River(world, source)
        river.flow()
        rivers.append(river)

    print neighbors(world['heightmap'], (10, 10), radius=2, sort=True)

    return rivers, world
