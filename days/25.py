from itertools import count
from functools import reduce

def decode(snafu):
    return sum((int(v) if v.isdigit() else -1 if v == '-' else -2) * (5 ** exp) for v, exp in zip(snafu[::-1], count()))

def encode(n):
    length = next(i for i in count(1) if sum(2 * (5 ** exp) for exp in range(i)) >= n)
    values = reduce(lambda acc, exp: [*acc, ((v + (5 ** (exp + 1))) if (v := ((n - sum(acc, 0) + 3 * (5 ** exp)) % (5 ** (exp + 1))) - 3 * (5 ** exp)) <= -(3 * (5 ** exp)) else v)], range(length), [])
    return ''.join(str(v) if (v := a // (5 ** exp)) >= 0 else '-' if v == -1 else '=' for a, exp in zip(values, count()))[::-1]

def first(lines):
    return encode(sum(map(decode, lines)))

def second(_):
    pass

example = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''