import random
import numpy as np
from terragen.utils import log

patterns = [
    # volcano
    [
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 1, 1, 1, 1, 1, 1, 0, 0 ],
        [ 0, 1, 1, 2, 2, 2, 2, 1, 1, 0 ],
        [ 0, 1, 2, 3, 3, 3, 3, 2, 1, 0 ],
        [ 0, 1, 2, 3, 1, 1, 3, 2, 1, 0 ],
        [ 0, 1, 2, 3, 1, 1, 3, 2, 1, 0 ],
        [ 0, 1, 2, 3, 3, 3, 3, 2, 1, 0 ],
        [ 0, 1, 1, 2, 2, 2, 2, 1, 1, 0 ],
        [ 0, 0, 1, 1, 1, 1, 1, 1, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    ],
    # crater
    [
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 1, 1, 1, 1, 1, 1, 0, 0 ],
        [ 0, 1, 3, 4, 4, 4, 4, 3, 1, 0 ],
        [ 0, 1, 4, 2, 2, 2, 2, 4, 1, 0 ],
        [ 0, 1, 4, 2, 0, 0, 2, 4, 1, 0 ],
        [ 0, 1, 4, 2, 0, 0, 2, 4, 1, 0 ],
        [ 0, 1, 4, 2, 2, 2, 2, 4, 1, 0 ],
        [ 0, 1, 3, 4, 4, 4, 4, 3, 1, 0 ],
        [ 0, 0, 1, 1, 1, 1, 1, 1, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    ],
    # peak
    [
        [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 0 ],
        [ 1, 2, 2, 2, 2, 2, 2, 2, 1, 1 ],
        [ 1, 2, 3, 3, 3, 3, 3, 2, 1, 1 ],
        [ 1, 2, 3, 4, 4, 4, 3, 2, 1, 1 ],
        [ 1, 2, 3, 4, 5, 4, 3, 2, 1, 1 ],
        [ 1, 2, 3, 4, 5, 4, 3, 2, 1, 1 ],
        [ 1, 2, 3, 4, 4, 4, 3, 2, 1, 1 ],
        [ 1, 2, 3, 3, 3, 3, 3, 2, 1, 1 ],
        [ 1, 2, 2, 2, 2, 2, 2, 2, 1, 1 ],
        [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 0 ],
    ]
]


def make_features(heightmap, size):
    num_features = random.randint(0, int(size / 9))

    log('Making %i terrain features' % num_features)

    feature_map = np.copy(heightmap)
    feature_image = np.zeros(heightmap.shape, dtype=bool)


    for i in xrange(num_features):
        feature = random.choice(patterns)
        height = len(feature)
        width = len(feature[0])

        x_, y_ = heightmap.shape

        j = 0
        k = 0

        start_x = random.randint(0, x_ - height)
        start_y = random.randint(0, y_ - width)

        for x in xrange(start_x, start_x + height - 1):
            k = 0
            for y in xrange(start_y, start_y + width - 1):
                feature_map[x, y] = heightmap[x, y] + feature[j][k] * 2
                feature_image[x, y] = True
                k += 1
            j += 1

    return feature_map, feature_image
