import numpy
import random

def create_random_func(noise_func, noise_min, noise_max):
    """ Factory function for the noise function """
    def height_func(i):
        return noise_func(noise_min*2**-i, noise_max*2**-i)
    return height_func

def make_space(width, height, height_func):
    """
    Make the array and fill the corners with random values. It's important in
    this step that the top edges are equal and the bottom edges are equal,
    since they wrap around.
    """
    space = numpy.zeros((width, height))
    space[0, 0] = height_func(0)
    space[0, -1] = height_func(0)
    space[-1, 0] = height_func(0)
    space[-1, -1] = height_func(0)
    return space

def avg(*args):
    """ Return the average of each argument. """
    return sum(args)/len(args)

def diamond_square(space, height_func):
    """ Combined iterative diamond and square step """
    x_max, y_max = space.shape
    x_min = y_min = 0
    x_max -= 1
    y_max -= 1

    side = x_max
    squares = 1
    i = 0

    while side > 1:
        for x in range(squares):
            for y in range(squares):
                # corner locations
                x_left = x*side
                x_right = (x+1)*side
                y_top = y*side
                y_bottom = (y+1)*side

                # sizes of halfs
                dx = side/2
                dy = side/2

                # midpoints
                xm = x_left + dx
                ym = y_top + dy

                # diamond step
                # create center avg for each square
                space[xm, ym] = avg(space[x_left, y_top],
                                    space[x_left, y_bottom],
                                    space[x_right, y_top],
                                    space[x_right, y_bottom])
                space[xm, ym] += height_func(i)

                # square step
                # create squares for each diamond
                # top square
                if (y_top - dy) < y_min:
                    temp = y_max - dy
                else:
                    temp = y_top - dy
                space[xm,y_top] = avg(space[x_left, y_top],
                                      space[x_right, y_top],
                                      space[xm, ym],
                                      space[xm, temp])
                space[xm,y_top] += height_func(i)

                # wrap the top edges around the center of the image
                # e.g north from Canada into Russia

                if y_top == y_min:
                    space[x_max - xm, y_top] = space[xm, y_top]


                # bottom square
                if (y_bottom + dy) > y_max:
                    temp = y_top + dy
                else:
                    temp = y_bottom - dy
                space[xm, y_bottom] = avg(space[x_left, y_bottom],
                                          space[x_right, y_bottom],
                                          space[xm, ym],
                                          space[xm, temp])
                space[xm, y_bottom] += height_func(i)

                # bottom wrapping part
                if y_bottom == y_max:
                    space[x_max - xm, y_bottom] = space[xm, y_bottom]

                # left square
                if (x_left - dx) < x_min:
                    temp = x_max - dx
                else:
                    temp = x_left - dx
                space[x_left, ym] = avg(space[x_left, y_top],
                                        space[x_left, y_bottom],
                                        space[xm, ym],
                                        space[temp, ym])
                space[x_left, ym] += height_func(i)

                # left wrapping
                if x_left == x_min:
                    space[x_max,ym] = space[x_left,ym]

                # right square
                if (x_right + dx) > x_max:
                    temp = x_min + dx
                else:
                    temp = x_right + dx
                space[x_right, ym] = avg(space[x_right, y_top],
                                         space[x_right, y_bottom],
                                         space[xm, ym],
                                         space[temp, ym])
                space[x_right, ym] += height_func(i)

                # right wrapping
                if x_right == x_max:
                    space[x_min,ym] = space[x_right,ym]

        # set up next steps
        side /= 2
        squares *= 2
        i += 1

def make_terrain(image, size=513):
    """
    Uses the diamond-square algorithm to generate a terrain map.
    Takes in a PIL image and applies the heightmap to that image.
    Returns a numpy array of int values from 0 to 255
    representing the heightmap.
    """
    noise_func = random.uniform
    noise_min = -1.0
    noise_max = 1.0
    height_func = create_random_func(noise_func, noise_min, noise_max)

    # initialize the space with random values on the corners
    space = make_space(size, size, height_func)

    # square diamond steps
    diamond_square(space, height_func)

    # convert to 255 2D array for the heightmap image
    c_min = min(space.flat)
    c_max = max(space.flat)
    x_, y_ = space.shape
    for x in xrange(x_):
        for y in xrange(y_):
            h = int(round(((space[x, y] + abs(c_min)) / (abs(c_min) + c_max)) * 255))
            image[x, y] = (h, h, h)
            space[x, y] = h

    return space

def make_groundwater(world):
    """
    Use the diamond-square algorithm to make groundwater
    """
    noise_func = random.uniform
    noise_min = -1.0
    noise_max = 1.0
    height_func = create_random_func(noise_func, noise_min, noise_max)

    # initialize the space with random values on the corners
    space = make_space(world['size'], world['size'], height_func)

    # square diamond steps
    diamond_square(space, height_func)

    # convert to 255 2D array for the heightmap image
    c_min = min(space.flat)
    c_max = max(space.flat)
    x_, y_ = space.shape
    for x in xrange(x_):
        for y in xrange(y_):
            if world['heightmap'][x, y] < world['sea_level']:
                space[x, y] = 0
            else:
                h = int(round(((space[x, y] + abs(c_min)) / (abs(c_min) + c_max)) * 15))
                if h < 5: # some land doesn't have groundwater
                    h = 0
                space[x, y] = h

    return space.astype(int)
