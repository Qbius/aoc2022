def mix(values, ntimes=1):
    indices = list(enumerate(values))
    length = len(indices)

    for _ in range(ntimes):
        for i in range(length):
            prev_pos, n = indices[i]
            new_pos = (prev_pos + n) % (length - 1)
            if new_pos == 0: new_pos = length - 1
            start, end, change = (prev_pos, new_pos, -1) if prev_pos < new_pos else (new_pos, prev_pos, 1)
            for j, (pos, k) in enumerate(indices):
                if pos >= start and pos <= end and pos != prev_pos:
                    indices[j] = (pos + change, k)
            indices[i] = (new_pos, n)

    return [v for _, v in sorted(indices)]

def first(values: int):
    mixed = mix(values)
    afterzero = lambda i: mixed[(mixed.index(0) + i) % len(mixed)]
    return afterzero(1000) + afterzero(2000) + afterzero(3000)
    

def second(values: int):
    ekey = 811589153
    mixed = mix([v * ekey for v in values], ntimes=10)
    afterzero = lambda i: mixed[(mixed.index(0) + i) % len(mixed)]
    return afterzero(1000) + afterzero(2000) + afterzero(3000)

example = '''1
2
-3
3
-2
0
4'''


'''
Initial arrangement:
1, 2, -3, 3, -2, 0, 4

1 moves between 2 and -3:
2, 1, -3, 3, -2, 0, 4

2 moves between -3 and 3:
1, -3, 2, 3, -2, 0, 4

-3 moves between -2 and 0:
1, 2, 3, -2, -3, 0, 4

3 moves between 0 and 4:
1, 2, -2, -3, 0, 3, 4

-2 moves between 4 and 1:
1, 2, -3, 0, 3, 4, -2

0 does not move:
1, 2, -3, 0, 3, 4, -2

4 moves between -3 and 0:
1, 2, -3, 4, 0, 3, -2
'''