from iteration_utilities import deepflatten
from pandas import Series

def parse(lines):
    rows = [row.split(' ') for row in lines]
    moves_stack = [((int(val_str) if dr in ['L', 'R'] else 0) * (1 if dr == 'R' else -1), (int(val_str) if dr in ['U', 'D'] else 0) * (1 if dr == 'D' else -1)) for dr, val_str in rows]
    return list(deepflatten([max(map(abs, move)) * [tuple(map(lambda e: e // max(map(abs, move)), move))] for move in moves_stack], ignore=tuple))

def first(moves):
    head = Series((0, 0))
    tail = Series((0, 0))
    visited = {tuple(tail)}
    for move in moves:
        head += move
        if (head - tail).abs().max() > 1:
            tail = head - move
            visited.add(tuple(tail))
    return len(visited)

def follow(head, tail):
    match head, tail:
        case (hx, hy), (tx, ty) if hx == tx and abs(hy - ty) == 2:
            return (tx, round((hy + ty) / 2))
        case (hx, hy), (tx, ty) if hy == ty and abs(hx - tx) == 2:
            return (round((hx + tx) / 2), ty)
        case (hx, hy), (tx, ty) if abs(hx - tx) <= 1 and abs(hy - ty) <= 1:
            return (tx, ty)
        case (hx, hy), (tx, ty):
            return (tx + (-1 if hx < tx else 1), ty + (-1 if hy < ty else 1))

def second(moves):
    rope = [(0, 0) for _ in range(10)]
    visited = {rope[-1]}
    for (mx, my) in moves:
        hx, hy = rope[0]
        rope[0] = (hx + mx, hy + my)
        for i in range(len(rope) - 1):
            rope[i + 1] = follow(rope[i], rope[i + 1])
            if i == (len(rope) - 2):
                visited.add(rope[-1])
    return len(visited)

example = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''