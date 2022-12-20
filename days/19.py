from common import regex, Pipe
from functools import cache
from time import time

pattern = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
def parse(blueprints_raw: regex(pattern, [int ,int, int, int, int, int, int])):
    return {bid: {'ore': ore_o, 'clay': clay_o, 'obsidian': (obsi_o, obsi_c), 'geode': (geode_o, geode_ob)} for bid, ore_o, clay_o, obsi_o, obsi_c, geode_o, geode_ob in blueprints_raw}

def consider_all(blueprint):
    oreocost = blueprint['ore']
    clayocost = blueprint['clay']
    obsiocost, obsiccost = blueprint['obsidian']
    geodeocost, geodeobcost = blueprint['geode']

    @cache
    def process(oren, clayn, obsin, geoden, orer, clayr, obsir, geoder, nextr, minute):
        if minute == 0:
            return geoden
        elif nextr == 'ore' and oren >= oreocost:
            return max(process(oren - oreocost + orer, clayn + clayr, obsin + obsir, geoden + geoder, orer + 1, clayr, obsir, geoder, n, minute - 1) for n in ['ore', 'clay', 'obsidian', 'geode'])
        elif nextr == 'clay' and oren >= clayocost:
            return max(process(oren - clayocost + orer, clayn + clayr, obsin + obsir, geoden + geoder, orer, clayr + 1, obsir, geoder, n, minute - 1) for n in ['ore', 'clay', 'obsidian', 'geode'])
        elif nextr == 'obsidian' and oren >= obsiocost and clayn >= obsiccost:
            return max(process(oren - obsiocost + orer, clayn - obsiccost + clayr, obsin + obsir, geoden + geoder, orer, clayr, obsir + 1, geoder, n, minute - 1) for n in ['ore', 'clay', 'obsidian', 'geode'])
        elif nextr == 'geode' and oren >= geodeocost and obsin >= geodeobcost:
            return max(process(oren - geodeocost + orer, clayn + clayr, obsin - geodeobcost + obsir, geoden + geoder, orer, clayr, obsir, geoder + 1, n, minute - 1) for n in ['ore', 'clay', 'obsidian', 'geode'])
        else:
            return process(oren + orer, clayn + clayr, obsin + obsir, geoden + geoder, orer, clayr, obsir, geoder, nextr, minute - 1)

    return max(process(0, 0, 0, 0, 1, 0, 0, 0, n, 24) for n in ['ore', 'clay', 'obsidian', 'geode'])

def timeit(binfo):
    start = time()
    consider_all(binfo)
    return time() - start

def first(blueprints):
    x = {b: consider_all(binfo) for b, binfo in list(blueprints.items())}
    print(x)

def second(values):
    pass

example = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''