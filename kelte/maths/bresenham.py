def bresenham(start, end):
    """Yield a line ray from start to end
    """
    ((x0, y0), (x1, y1)) = (start, end)
    dx, dy = (x1 - x0), (y1 - y0)

    x_step, dx = (1, dx) if dx >= 0 else (-1, -dx)
    y_step, dy = (1, dy) if dy >= 0 else (-1, -dy)

    if dx > dy:
        xx, xy, yx, yy = x_step, 0, 0, y_step
    else:
        dx, dy = dy, dx  # note the swap here
        xx, xy, yx, yy = 0, y_step, x_step, 0

    error = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x * xx + y * yx, y0 + x * xy + y * yy
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
