from re import search

class raw_input:
    pass

class RegexBase:
    pass

def regex(pattern, types):
    return type('', (RegexBase,), {'process': lambda lines: [[arg_type(arg) for arg, arg_type in zip(search(pattern, line).groups(), types)] for line in lines]})

class SingleLineBase:
    pass

def single_line(delimiter, typ):
    return type('', (SingleLineBase,), {'process': lambda raw_input: list(map(typ, raw_input.strip().split(delimiter)))})

class Pipe(object):
    map = lambda f: lambda l: list(map(f, l))
    filter = lambda f: lambda l: list(filter(f, l))

    def __init__(self, obj):
        self.obj = obj
        self.fs = []

    def __or__(self, callee):
        if callee is print:
            return self.obj
        else:
            self.obj = callee(self.obj)
            return self

P = Pipe

def djikstra(start, points, nbrs_getter=None):
    if nbrs_getter is None:
        dimcount = len(list(points)[0])
        elebase = [0, 0] * dimcount
        bases = [[*elebase[:i * 2], -1, 1, *elebase[(i + 1) * 2:]] for i in range(dimcount)]
        directions = list(zip(*bases))
        nbrs_getter = lambda p: [nbr for dr in directions if (nbr := tuple(map(sum, zip(p, dr)))) in points]

    distances = {point: len(points) + 1 for point in points}
    distances[start] = 0
    visited = set()
    not_visited = lambda point: point not in visited
    while visited != points:
        current = min(filter(not_visited, distances), key=distances.get)
        for nbr in nbrs_getter(current):
            if nbr not in visited:
                distances[nbr] = distances[current] + 1
        visited.add(current)
    return distances

def take(iterable, n):
    return [next(iterable) for _ in range(n)]