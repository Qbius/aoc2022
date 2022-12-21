from itertools import count, pairwise
from numpy import sign

def parse(lines):
    corners = [[tuple(map(int, point.split(','))) for point in line.split(' -> ')] for line in lines]
    point_range = lambda n: range(0, n + sign(n), sign(n))
    return set().union(*[{(sx + i * abs(sign(ex - sx)), sy + i * abs(sign(ey - sy))) for (sx, sy), (ex, ey) in pairwise(line) for i in point_range(ex + ey - sx - sy)} for line in corners])

def fall_path(start, grid):
    bottom = max(y for _x, y in grid)
    possibilities = lambda x, y: [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
    while (next_spot := next((p for p in possibilities(*start) if p[1] <= bottom and p not in grid), None)) is not None:
        start = next_spot
    
    return grid | ({start} if start[1] < bottom else set())

def first(grid):
    rocks = len(grid)
    for i in count():
        new_grid = fall_path((500, 0), grid)
        if len(new_grid) == len(grid):
            break
        else:
            grid = new_grid
    return len(grid) - rocks

def add_floor(grid):
    floor_y = max(y for _x, y in grid) + 2
    return {(500 + i, floor_y) for i in range(-floor_y - 1, floor_y + 2)}

def second(grid):
    grid = grid | add_floor(grid)
    rocks = len(grid)
    for i in count():
        new_grid = fall_path((500, 0), grid)
        if (500, 0) in new_grid:
            break
        else:
            grid = new_grid
    return len(grid) - rocks + 1

example = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''