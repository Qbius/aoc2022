from pandas import DataFrame
from math import prod
from common import raw_input

def parse(lines):
    return [list(map(int, line)) for line in lines]

def visible_from_sides(grid):
    return {(w, h) for h, row in enumerate(grid) for w, n in enumerate(row) if max(row[:w], default=-1) < n or max(row[w + 1:], default=-1) < n}

def visible_from_topbot(grid):
    return {(h, w) for w, h in visible_from_sides(list(zip(*grid)))}

def first(grid):
    return len(visible_from_sides(grid) | visible_from_topbot(grid))

def scenic_left(grid):
    results = []
    for i in range(10):
        results.append([])
        for row in grid:
            results[-1].append([])
            goode = 0
            for n in row:
                results[-1][-1].append(goode)
                if n < i:
                    goode += 1
                elif n == i:
                    goode = 1
                else:
                    goode = 1
    return list(map(DataFrame, results))

def scenic_right(grid):
    left = scenic_left([row[::-1] for row in grid])
    for i, df in enumerate(left):
        left[i] = df.iloc[:, ::-1]
        left[i].columns = df.columns
    return left

def scenic_top(grid):
    return [df.T for df in scenic_left(list(zip(*grid)))]

def scenic_bottom(grid):
    return [df.T for df in scenic_right(list(zip(*grid)))]

def ex_tables(grid):
    df = DataFrame(grid)
    return [(df == i).applymap(int) for i in range(10)]

def second(grid):
    return sum(prod(group) for group in zip(scenic_left(grid), scenic_right(grid), scenic_top(grid), scenic_bottom(grid), ex_tables(grid))).max().max()

example = '''30373
25512
65332
33549
35390'''