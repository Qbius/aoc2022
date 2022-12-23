from collections import Counter
from itertools import count

def parse(lines):
    return {(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == '#'}

moves = [
    ((0, -1), [(-1, -1), (0, -1), (1, -1)]),
    ((0, 1), [(-1, 1), (0, 1), (1, 1)]),
    ((-1, 0), [(-1, -1), (-1, 0), (-1, 1)]),
    ((1, 0), [(1, -1), (1, 0), (1, 1)]),
]
combine = lambda a, b: tuple(map(sum, zip(a, b)))

def try_move(elf, startmove, elves):
    adjs = {combine((x, y), elf) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0}
    if len(adjs & elves) == 0:
        return elf

    for i in range(len(moves)):
        move, checks = moves[(startmove + i) % len(moves)]
        checks = set(map(lambda t: combine(t, elf), checks))
        if len(checks & elves) == 0:
            return combine(elf, move)
    return elf

def rounds(elves, n=None):
    prev = set()
    for r in count():
        if elves == prev or (n is not None and r >= n):
            return r, elves

        prev = elves
        new_elves = {e: try_move(e, r % len(moves), elves) for e in elves}
        contested = {ne for ne, count in Counter(new_elves.values()).items() if count > 1}
        elves = {e if ne in contested else ne for e, ne in new_elves.items()}
    
def empty_space(elves):
    (minx, miny), (maxx, maxy) = list(map(min, zip(*elves))), list(map(max, zip(*elves)))
    return (maxx - minx + 1) * (maxy - miny + 1) - len(elves)

def first(elves):
    _, elves = rounds(elves, 10)
    return empty_space(elves)

def second(elves):
    r, _ = rounds(elves)
    return r

example = '''....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..'''