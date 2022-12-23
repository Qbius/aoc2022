from common import raw_input
import re

def parse(rawinpt: raw_input):
    themap_raw, directions_raw = rawinpt.split('\n\n')
    themap = {(x, y): c for y, mapline in enumerate(themap_raw.split('\n')) for x, c in enumerate(mapline) if c in ['.', '#']}
    directions = [int(bit) if bit.isdigit() else bit for bit in re.findall(r'\d+|L|R', directions_raw)]
    return themap, directions

faces = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def traverse(current, facing, themap):
    nextry = tuple(map(sum, zip(current, facing)))
    if nextry not in themap:
        dirf = min if sum(facing) > 0 else max
        samebar = lambda p: (p[0] == current[0]) if facing[0] == 0 else (p[1] == current[1])
        nextry = dirf([(x, y) for x, y in themap.keys() if samebar((x, y))])
    return nextry if themap[nextry] != '#' else current

def first(themap, directions):
    current = min(themap.keys(), key=lambda t: (t[1], t[0]))
    facing = faces[0]
    
    for d in directions:
        match d:
            case steps if isinstance(steps, int):
                for _ in range(steps):
                    current = traverse(current, facing, themap)
            case 'R':
                facing = faces[(faces.index(facing) + 1) % len(faces)]
            case 'L':
                facing = faces[(faces.index(facing) - 1) % len(faces)]

    column, row = current
    print(row, column)
    return 1000 * (row + 1) + 4 * (column + 1) + faces.index(facing)

def second(themap, directions):
    pass

example = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''