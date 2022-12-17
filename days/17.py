from itertools import count, cycle
from common import raw_input

shapes = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, -2), (0, -1), (1, -1), (2, -1), (1, 0)},
    {(2, -2), (2, -1), (0, 0), (1, 0), (2, 0)},
    {(0, -3), (0, -2), (0, -1), (0, 0)},
    {(0, -1), (1, -1), (0, 0), (1, 0)},
]

dirdict = {
    '>': (1, 0),
    '<': (-1, 0),
    'down': (0, 1),
}

def shape_gen():
    for shape in cycle(shapes):
        yield shape

combine = lambda *args: tuple(map(sum, zip(*args)))

class Kekris(object):
    def __init__(self, wind, minx, maxx):
        self.wind = wind
        self.minx = minx
        self.maxx = maxx
        self.place = {(x, 0) for x in range(minx, maxx + 1)}
        self.gen = shape_gen()
        self.simulated = 0
        self.prev_peak = 0
        self.height_history = []
        self.cycle = None
        self.goal = 0
        self.acctocycle = None

    def find_cycles(self):
        if self.acctocycle is None and len(self.height_history) >= 15:
            for cyclelength in range(5, len(self.height_history) // 3 + 1):
                flast = self.height_history[1 * -cyclelength:]
                slast = self.height_history[2 * -cyclelength:1 * -cyclelength]
                tlast = self.height_history[3 * -cyclelength:2 * -cyclelength]
                if tlast == slast and slast == flast:
                    head = self.height_history[:len(self.height_history) - cyclelength * 3]
                    tailn = self.goal - len(head) + 1
                    self.acctocycle = sum(head) + sum(tlast) * (tailn // cyclelength) + sum(tlast[:tailn % cyclelength])

    def peak(self):
        return -min(y for _, y in self.place)

    def new_shape(self):
        shape = next(self.gen)
        self.simulated += 1
        peak = self.peak()
        self.height_history.append(peak - self.prev_peak)
        self.prev_peak = peak
        self.find_cycles()
        return {(x + 2, y - 4 - peak) for x, y in shape}

    def move(self, shape, direction):
        moved_shape = {combine(point, dirdict[direction]) for point in shape}
        intersects = len(moved_shape & self.place) > 0
        out_of_bounds = any(x < self.minx or x > self.maxx for x, _ in moved_shape)
        if not intersects and not out_of_bounds:
            return moved_shape
        elif direction != 'down':
            return shape
        else:
            self.place = self.place | shape
            return self.new_shape()

    def simulate(self, n):
        self.goal = n
        shape = self.new_shape()
        for turn in count():
            if self.acctocycle is not None:
                return self.acctocycle
            elif self.simulated > n:
                return self.peak()
            else:
                shape = self.move(shape, self.wind[turn % len(self.wind)])
                shape = self.move(shape, 'down')

def first(wind: raw_input):
    simulation = Kekris(wind, minx=0, maxx=6)
    return simulation.simulate(2022)

def second(wind: raw_input):
    simulation = Kekris(wind, minx=0, maxx=6)
    return simulation.simulate(1000000000000)
    
example = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

