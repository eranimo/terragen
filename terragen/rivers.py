import numpy as np
from random import randint
from terragen.utils import log

def make_rivers(world):
    mountain_cutoff = world['max_height'] - 15
    mountains = np.transpose(np.nonzero(world['heightmap'] >= mountain_cutoff))

    log('%i mountains or %0.5f%%' %
        (len(mountains), (float(len(mountains)) / float(world['size']**2)) * 100))

    num_rivers = 1 # randint(0, int(len(mountains) * 0.10))
    log('Making %i rivers' % num_rivers)
