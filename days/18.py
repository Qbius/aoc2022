from common import regex
from sys import setrecursionlimit
setrecursionlimit(2500)

def is_adjacent(a, b, points2sums):
    diff1 = abs(points2sums[a] - points2sums[b]) == 1
    eqal2 = len([None for ap, bp in zip(a, b) if ap == bp]) == 2
    return diff1 and eqal2

def first(points: regex(r'(\d+),(\d+),(\d+)', [int, int, int])):
    points = list(map(tuple, points))
    points2sums = {point: sum(point) for point in points}
    blocked_sides = {point: len([p for p in points if is_adjacent(point, p, points2sums)]) for point in points}
    return len(points) * 6 - sum(blocked_sides.values())

def get_bubbles(points, i1, i2, isort):
    raw_list = [((p[i1], p[i2]), p[isort]) for p in points]
    unique = dict(raw_list).keys()
    all_applicable = {u: [v for desc, v in raw_list if desc == u] for u in unique}
    bubbles_packed = {u: set(range(min(ps), max(ps) + 1)) - set(ps) for u, ps in all_applicable.items()}
    return {tuple(n for _, n in sorted([(i1, a), (i2, b), (isort, v)])) for (a, b), vs in bubbles_packed.items() for v in vs}
    
def get_confined(points):
    return get_bubbles(points, 0, 1, 2) & get_bubbles(points, 0, 2, 1) & get_bubbles(points, 1, 2, 0)

def filter_open(air, solid):
    considered = set()
    dirs = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    def is_enclosed(point):
        if point in considered:
            return True
        else:
            considered.add(point)
            adjs = [tuple(map(sum, zip(point, diff))) for diff in dirs]
            return all(adj in solid or (adj in air and is_enclosed(adj)) for adj in adjs)
    return set(filter(is_enclosed, air))

def second(points: regex(r'(\d+),(\d+),(\d+)', [int, int, int])):
    points = list(map(tuple, points))
    solid = set(points)
    air = get_confined(points)
    filtered_air = filter_open(air, solid)
    return first(solid) - first(filtered_air)

example = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''