from PIL import Image

def draw_image(array, get_func, color_func, name, size):
    """
    Draws an image based on an array of values, with a function to interpret those values,
    and a color function to interpret that value into an RGB color tuple.
    """
    img = Image.new('RGB', (size, size), "black")
    img_map = img.load()

    x_, y_ = array.shape
    for x in xrange(x_):
        for y in xrange(y_):
            cell = array[x, y]
            img_map[x, y] = color_func(get_func(cell), x, y)

    img.save('images/'+name+'.png')
