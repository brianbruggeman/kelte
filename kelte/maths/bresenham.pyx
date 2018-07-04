# cython: boundscheck=False
# cython: wraparound=False


def bresenham(start, end):
    """Yield a line ray from start to end
    """
    cdef:
        int x0 = start[0]
        int y0 = start[1]
        int x1 = end[0]
        int y1 = end[1]

        int dx = x1 - x0
        int dy = y1 - y0

        int x_step = 1
        int y_step = 1

        int xx = 0
        int xy = 0
        int yx = 0
        int yy = 0

        int error = 0
        int y = 0
        int x = 0

    if dx < 0:
        x_step = -1
        dx = -dx

    if dy < 0:
        y_step = -1
        dy = -dy

    if dx > dy:
        xx = x_step
        yy = y_step

    else:
        dx, dy = dy, dx  # note the swap here
        xy = y_step
        yx = x_step

    error = 2 * dy - dx
    for x in range(dx + 1):
        point = x0 + x * xx + y * yx, y0 + x * xy + y * yy
        yield point
        if error >= 0:
            y += 1
            error = error - 2 * dx
        error = error + 2 * dy


if __name__ == '__main__':
    import random
    from kelte.vendored import click

    @click.command()
    @click.argument('x0', default=random.randint(0, 80), type=int)
    @click.argument('y0', default=random.randint(0, 50), type=int)
    @click.argument('x1', default=random.randint(0, 80), type=int)
    @click.argument('y1', default=random.randint(0, 50), type=int)
    def cli(x0, x1, y0, y1):
        start, end = (x0, y0), (x1, y1)

        print(f'path: {start} -> {end}')
        for point in bresenham(start, end):
            print(point)

    cli()
