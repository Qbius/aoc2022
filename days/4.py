from common import regex

def first(values: regex(r'(\d+)-(\d+),(\d+)-(\d+)', [int, int, int, int])):
    grouped = [sorted([(a, b), (c, d)], key=lambda t: t[1] - t[0]) for a, b, c, d in values]
    return len([None for (a, b), (c, d) in grouped if a >= c and b <= d])

def second(values: regex(r'(\d+)-(\d+),(\d+)-(\d+)', [int, int, int, int])):
    grouped = [sorted([(a, b), (c, d)]) for a, b, c, d in values]
    return len([None for (a, b), (c, d) in grouped if b >= c])

example = '''
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''