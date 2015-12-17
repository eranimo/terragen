import numpy as np
from random import randint
from terragen.utils import log, find_neighbors, cell_north, cell_east, cell_west, cell_south


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
        super(RiverSegment, self).__init__(river)
        self.location = location
        self.elevation = river.world['heightmap'][location[0], location[1]]
        self.river.world['river_array'][location[0], location[1]] = True

    def next(self, last_elevation=None):
        if last_elevation is None:
            last_elevation = self.elevation
        elevation, x, y = find_neighbors(self.river.world['heightmap'],
                                         self.location,
                                         sort=True)[0]
        print self.elevation, elevation, x, y
        if self.river.world['river_array'][x][y]:
            # neighbor is a river segment
            print('encountered river at ', x, y)
            return False
        # if elevation == self.elevation:
        #     print("Making a lake at %i, %i" % (x, y))
        #     lake = Lake(self.river, (x, y), self.elevation)
        #     self.next_segments.append(lake)
        #     lake.fill()
        if elevation <= last_elevation and  elevation > self.river.world['sea_level']:
            segment = RiverSegment(self.river, (x, y))
            self.next_segments.append(segment)
            segment.next(elevation)
        else:
            print('Reached sea level')



class Lake(RiverPart):
    def __init__(self, river, location, elevation):
        super(Lake, self).__init__(river)
        self.location = location
        self.parts = set([location])
        self.elevation = elevation
        self.river.world['river_array'][location[0], location[1]] = True

    def fill(self):
        def fill_step(target, elev, check=True):
            if check and elev >= self.elevation:
                return False
            if target in self.parts:
                print target, self.parts
                return False
            print('river segment', target)
            self.parts.add(target)
            self.river.world['river_array'][target[0], target[1]] = True
            cell, x, y = cell_north(self.river.world['heightmap'], target[0], target[1])
            fill_step((x, y), cell)
            cell, x, y = cell_south(self.river.world['heightmap'], target[0], target[1])
            fill_step((x, y), cell)
            cell, x, y = cell_east(self.river.world['heightmap'], target[0], target[1])
            fill_step((x, y), cell)
            cell, x, y = cell_west(self.river.world['heightmap'], target[0], target[1])
            fill_step((x, y), cell)
        # fill_step((self.parts[0][0], self.parts[0][1]), self.elevation, check=False)

        cell, x, y = cell_north(self.river.world['heightmap'], self.location[0], self.location[1])
        fill_step((x, y), cell)
        cell, x, y = cell_south(self.river.world['heightmap'], self.location[0], self.location[1])
        fill_step((x, y), cell)
        cell, x, y = cell_east(self.river.world['heightmap'], self.location[0], self.location[1])
        fill_step((x, y), cell)
        cell, x, y = cell_west(self.river.world['heightmap'], self.location[0], self.location[1])
        fill_step((x, y), cell)

class River:
    def __init__(self, world, location):
        self.world = world
        self.source = RiverSegment(self, location) # river segment

        self.source.next()

    def flow(self):
        """ Iterate over the river, eroding and depositing sedements. """
        pass

def river_branch(world, start_location):
    x, y = start_location
    current_elevation = world['heightmap'][x, y]
    sea_level = world['sea_level']
    while current_elevation >= sea_level:
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

    num_rivers = randint(0, int(len(mountains) * 0.10))
    log('Making %i rivers' % num_rivers)
    river_sources = mountains[:num_rivers]

    # since rivers look the same on the images, this is a boolean array
    world['river_array'] = np.zeros(world['heightmap'].shape, dtype=np.bool)

    def get_elevation(loc):
        return world['heightmap'][loc[0], loc[1]]

    def is_river(loc):
        return world['river_array'][loc[0], loc[1]] is True

    def make_river_segment(loc):
        print(loc)
        world['river_array'][loc[0], loc[1]] = True

    rivers = []
    for source in river_sources:
        current_location = source
        current_elevation = get_elevation(current_location)
        can_continue = True
        while current_elevation >= world['sea_level'] and can_continue:


            # get neighboring pixels
            neighbors = find_neighbors(world['heightmap'],
                                       current_location,
                                       sort=True)[0]
            # lowest neighbor is higher  than me
            # if neighbors[0] > current_elevation):
            #     # make a lake here
            #     pass
            next_segment = neighbors[1], neighbors[2]
            # Is there a river here?
            if is_river(next_segment):
                print('River found at %i, %i', current_location)
                can_continue = False
            make_river_segment(current_location)
            current_location = next_segment
            current_elevation = get_elevation(current_location)

        # river = River(world, source)
        # river.flow()
        # world = river.world
        # rivers.append(river)


    return rivers, world
