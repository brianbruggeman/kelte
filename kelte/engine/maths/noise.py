import random

import numpy as np


def perlin(samples=None, seed=None, size=None):
    # permutation table
    size = 256 if size is None else size
    samples = 100 if samples is None else samples
    seed = random.randint(0, size) if seed is None else seed
    np.random.seed(seed)
    lin = np.linspace(0, 5, samples, endpoint=False)
    x, y = np.meshgrid(lin, lin[::-1])

    # grab 256 random values
    p = np.arange(size, dtype=int)
    np.random.shuffle(p)

    p = np.stack([p, p]).flatten()

    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)

    # internal coordinates
    xf = x - xi
    yf = y - yi

    # fade factors
    u = fade(xf)
    v = fade(yf)

    # noise components
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)

    # linear interpolation of noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)

    final = lerp(x1, x2, v)
    return final


def lerp(a, b, x):
    return a + x * (b - a)


def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y
