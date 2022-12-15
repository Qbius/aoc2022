from common import regex
from itertools import starmap, pairwise
from sys import argv

def manhattan(sx, sy, bx, by):
    return ((sx, sy), abs(bx - sx) + abs(by - sy))

def overlap(intervals):
    for i, ((fs, fe), (ss, se)) in enumerate(pairwise(intervals)):
        if ss < fe:
            return overlap([(min(fs, ss), max(fe, se)), *intervals[i + 2:]])
        else:
            return [(fs, fe), *overlap(intervals[i + 1:])]
    return intervals

def check_for_y(y, distances):
    intervals = [(sx - v_dist, sx + v_dist) for (sx, sy), dist in distances.items() if (v_dist := (dist - abs(y - sy))) >= 0]
    intervals.sort()
    return sum(x1 - x0 for x0, x1 in overlap(intervals))

def first(values: regex(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', [int, int, int, int])):
    distances = dict(starmap(manhattan, values))
    y = 10 if '-e' in argv or '--example' in argv else 2000000
    return check_for_y(y, distances)

def check_for_y2(y, distances, maxrange):
    intervals = [(max(sx - v_dist, 0), min(sx + v_dist, maxrange)) for (sx, sy), dist in distances.items() if (v_dist := (dist - abs(y - sy))) >= 0]
    intervals.sort()
    habited_count = sum(x1 - x0 for x0, x1 in overlap(intervals))
    res = set(range(maxrange + 1)) - set().union(*[set(range(i_s, i_e + 1)) for i_s, i_e in intervals]) if habited_count < maxrange else set()
    return {(x, y) for x in res}

def second(values: regex(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', [int, int, int, int])):
    distances = dict(starmap(manhattan, values))
    beacons = {(bx, by) for _sx, _sy, bx, by in values}
    maxrange = 20 if '-e' in argv or '--example' in argv else 4000000
    unihbaited = set().union(*[check_for_y2(i, distances, maxrange) for i in range(maxrange + 1)])
    x, y = list(unihbaited - beacons)[0]
    return x * 4000000 + y

example = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''