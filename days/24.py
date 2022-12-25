from common import take
from itertools import cycle

def parse(lines):
    dirs = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}
    blizzards = [((x, y + 1), dirs[c]) for y, (_wall1, *middle, _wall2) in enumerate(lines[1:-1]) for x, c in enumerate(middle) if c != '.']
    width = len(lines[0]) - 2
    height = len(lines) - 2
    perturns = list(zip(*[[((x + xdiff * i) % width, ((y + ydiff * i - 1) % height) + 1) for i in range(width * height)] for (x, y), (xdiff, ydiff) in blizzards]))
    n = 2000
    return take(cycle(perturns), n), width, height

def djikstra(start, points, stop):
    max_distance = len(points) + 1
    distances = {point: max_distance for point in points}
    distances[start] = 0
    visited = set()
    not_visited = lambda point: point not in visited
    while True:
        current = min(filter(not_visited, distances), key=distances.get)
        x, y, step = current
        if (x, y) == stop and distances[current] < max_distance:
            return distances[current]
        nbrs = [(x, y, step + 1), (x - 1, y, step + 1), (x + 1, y, step + 1), (x, y - 1, step + 1), (x, y + 1, step + 1)]
        for nbr in nbrs:
            if nbr not in visited and nbr in points:
                distances[nbr] = distances[current] + 1
        visited.add(current)

def first(perturns, width, height):
    grid = set().union(*[{(a, b, step) for a, b in (({(x, y + 1) for x in range(width) for y in range(height)} | {(0, 0), (width - 1, height + 1)}) - set(blizzards))} for step, blizzards in enumerate(perturns)])
    return djikstra((0, 0, 0), grid, (width - 1, height + 1))

def second(perturns, width, height):
    grid1 = set().union(*[{(a, b, step) for a, b in (({(x, y + 1) for x in range(width) for y in range(height)} | {(0, 0), (width - 1, height + 1)}) - set(blizzards))} for step, blizzards in enumerate(perturns)])
    one = djikstra((0, 0, 0), grid1, (width - 1, height + 1))

    print(one)
    grid2 = set().union(*[{(a, b, step) for a, b in (({(x, y + 1) for x in range(width) for y in range(height)} | {(0, 0), (width - 1, height + 1)}) - set(blizzards))} for step, blizzards in enumerate(perturns[one:])])
    two = djikstra((width - 1, height + 1, 0), grid2, (0, 0))

    print(two)
    grid3 = set().union(*[{(a, b, step) for a, b in (({(x, y + 1) for x in range(width) for y in range(height)} | {(0, 0), (width - 1, height + 1)}) - set(blizzards))} for step, blizzards in enumerate(perturns[one + two:])])
    three = djikstra((0, 0, 0), grid3, (width - 1, height + 1))

    print(one, two, three)
    return one + two + three

example = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''