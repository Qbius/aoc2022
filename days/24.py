from common import take
from itertools import cycle

def parse(lines):
    dirs = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}
    blizzards = [((x, y), dirs[c]) for y, (_wall1, *middle, _wall2) in enumerate(lines[1:-1]) for x, c in enumerate(middle) if c != '.']
    width = len(lines[0]) - 2
    height = len(lines) - 2
    perturns = list(zip(*[[((x + xdiff * i) % width, (y + ydiff * i) % height) for i in range(width * height)] for (x, y), (xdiff, ydiff) in blizzards]))
    n = 2000
    return take(cycle(perturns), n), width, height

from time import time
def djikstra(start, points, width, height, stop):
    startt = time()
    distances = {point: len(points) + 1 for point in points}
    distances[start] = 0
    visited = set()
    not_visited = lambda point: point not in visited
    while True:
        current = min(filter(not_visited, distances), key=distances.get)
        x, y, step = current
        if (x, y) == stop:
            print(current)
            return distances
        nbrs = [(x, y, step + 1), (x - 1, y, step + 1), (x + 1, y, step + 1), (x, y - 1, step + 1), (x, y + 1, step + 1)]
        for nbr in nbrs:
            if nbr not in visited and nbr in points:
                distances[nbr] = distances[current] + 1
        visited.add(current)
    return distances

def first(perturns, width, height):
    grid = set().union(*[{(a, b, step) for a, b in ({(x, y) for x in range(width) for y in range(height)} - set(blizzards))} for step, blizzards in enumerate(perturns)])
    distances = djikstra((0, 0, 0), grid, width, height, (width - 1, height - 1))
    return next(d for (x, y, step), d in distances.items() if x == (width - 1) and y == (height - 1) and d < (len(grid) + 1)) + 1

def second(perturns, width, height):
    grid1 = set().union(*[{(a, b, step) for a, b in ({(x, y) for x in range(width) for y in range(height)} - set(blizzards))} for step, blizzards in enumerate(perturns)])
    distances1 = djikstra((0, 0, 0), grid1, width, height, (width - 1, height - 1))
    one = next(d for (x, y, step), d in distances1.items() if x == (width - 1) and y == (height - 1) and d < (len(grid1) + 1)) + 1

    print(one)
    grid2 = set().union(*[{(a, b, step) for a, b in ({(x, y) for x in range(width) for y in range(height)} - set(blizzards))} for step, blizzards in enumerate(perturns[one + 1:])])
    distances2 = djikstra((width - 1, height - 1, 0), grid2, width, height, (0, 0))
    two = next(d for (x, y, step), d in distances2.items() if x == 0 and y == 0 and d < (len(grid2) + 1)) + 1

    print(two)
    grid3 = set().union(*[{(a, b, step) for a, b in ({(x, y) for x in range(width) for y in range(height)} - set(blizzards))} for step, blizzards in enumerate(perturns[one + two + 2:])])
    distances3 = djikstra((0, 0, 0), grid3, width, height, (width - 1, height - 1))
    three = next(d for (x, y, step), d in distances3.items() if x == (width - 1) and y == (height - 1) and d < (len(grid3) + 1)) + 1

    print(one, two, three)
    return one + two + three

example = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''