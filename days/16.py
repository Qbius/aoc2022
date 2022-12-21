import re
from time import time
from functools import cache
from common import raw_input

def parse(rawinpt: raw_input):
    pattern = r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(?:\, [A-Z]{2})*)'
    rates = {valve: int(rate_str) for valve, rate_str, _ in re.findall(pattern, rawinpt)}
    moves = {valve: adjs_str.split(', ') for valve, _, adjs_str in re.findall(pattern, rawinpt)}
    return rates, moves

def shortest_path(start, end, moves):
    max_distance = len(moves) + 1
    distances = {valve: max_distance for valve in moves}
    distances[start] = 0
    paths = {}
    paths[start] = [start]
    visited = set()
    while end not in visited:
        current = min([v for v in distances if v not in visited], key=distances.get)
        for point in [v for v in moves[current] if v not in visited]:
            distances[point] = distances[current] + 1
            paths[point] = [*paths[current], point]
        visited.add(current)
    return paths[end]

def crawl3(shortest_paths, rates):
    @cache
    def inner(valve, minutes, opened):
        available = [(adj, path) for adj, path in shortest_paths[valve].items() if adj not in opened and len(path) < minutes]
        return max([(minutes - len(path)) * rates[adj] + inner(adj, minutes - len(path), tuple([*opened, adj])) for adj, path in available], default=0)
    return inner('AA', 30, tuple())
    
def first(rates, moves):
    nicevalves = [valve for valve, rate in rates.items() if rate > 0]
    shortest_paths = {v: {ov: shortest_path(v, ov, moves) for ov in (set(nicevalves) - {v})} for v in ['AA', *nicevalves]}
    return crawl3(shortest_paths, rates)

def crawl4(shortest_paths, rates):
    @cache
    def inner(dest1, left1, dest2, left2, minute, opened):
        if minute == 0: return 0
        av1 = [(dest1, left1 - 1)] if (left1 > 0 or dest1 not in opened) and dest1 != 'AA' else [(adj, len(path) - 2) for adj, path in shortest_paths[dest1].items() if adj not in opened and len(path) < minute and adj != dest2]
        av2 = [(dest2, left2 - 1)] if (left2 > 0 or dest2 not in opened) and dest2 != 'AA' else [(adj, len(path) - 2) for adj, path in shortest_paths[dest2].items() if adj not in opened and len(path) < minute and adj != dest1]
        new_opened = tuple([*list(opened), *([dest1] if left1 == 0 and rates[dest1] else []), *([dest2] if left2 == 0 and rates[dest2] else [])])
        return sum(map(rates.get, opened)) + max((inner(adj1, lf1, adj2, lf2, minute - 1, new_opened) for adj1, lf1 in (av1 or [('x', 1000)]) for adj2, lf2 in ([e for e in av2 if adj1 != e[0]] or [('y', 1000)])), default=0)
    return inner('AA', 0, 'AA', 0, 26, tuple())
    

# def crawl4(shortest_paths, rates):
#     pathsum = lambda a, b: (a[0] + b[0], a[1] + b[1])
#     def inner(dest1, left1, dest2, left2, minute, opened):
#         if minute == 0: return (0, [])
#         av1 = [(dest1, left1 - 1)] if (left1 > 0 or dest1 not in opened) and dest1 != 'AA' else [(adj, len(path) - 2) for adj, path in shortest_paths[dest1].items() if adj not in opened and len(path) < minute and adj != dest2]
#         av2 = [(dest2, left2 - 1)] if (left2 > 0 or dest2 not in opened) and dest2 != 'AA' else [(adj, len(path) - 2) for adj, path in shortest_paths[dest2].items() if adj not in opened and len(path) < minute and adj != dest1]
#         new_opened = tuple([*list(opened), *([dest1] if left1 == 0 and rates[dest1] else []), *([dest2] if left2 == 0 and rates[dest2] else [])])
#         return pathsum((sum(map(rates.get, opened)), [(dest1, dest2, opened)]), max((inner(adj1, lf1, adj2, lf2, minute - 1, new_opened) for adj1, lf1 in (av1 or [('x', 1000)]) for adj2, lf2 in ([e for e in av2 if adj1 != e[0]] or [('y', 1000)])), default=(0, [])))
#     rate_up_to, path = inner('AA', 0, 'AA', 0, 26, tuple())
#     print(rate_up_to)
#     return path

def second(rates, moves):
    start = time()
    nicevalves = [valve for valve, rate in rates.items() if rate > 0]
    shortest_paths = {v: {ov: shortest_path(v, ov, moves) for ov in (set(nicevalves) - {v})} for v in ['AA', *nicevalves]}
    result = crawl4(shortest_paths, rates)
    print(f'{time() - start} seconds')
    return result

example = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''