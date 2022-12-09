from iteration_utilities import deepflatten
from pandas import Series
from copy import copy

def parse(rawinpt):
    rows = [row.split(' ') for row in rawinpt.split('\n')]
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

def second(moves):
    rope = [Series((0, 0)) for _ in range(10)]
    visited = {tuple(rope[-1])}
    for move in moves:
        rope[0] += move
        for i in range(len(rope) - 1):
            if (rope[i] - rope[i + 1]).abs().max() > 1:
                prev = copy(rope[i + 1])
                rope[i + 1] = rope[i] - move
                move = tuple(rope[i + 1] - prev)
                if i == (len(rope) - 1):
                    visited.add(tuple(rope[-1]))
        print(rope)
    return len(visited)

example = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''