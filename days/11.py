import re
from copy import copy
from math import prod

def parse(rawinpt):
    pattern = r'Monkey (\d+):\s+Starting items: (\d+(?:, \d+)*)\s+Operation: new = old (.) (\d+|old)\s+Test: divisible by (\d+)\s+If true: throw to monkey (\d+)\s+If false: throw to monkey (\d+)'
    return dict(sorted([
        (int(m_id), {
            'items': list(map(int, items_str.split(', '))),
            'f': eval(f'lambda old: old {op} {operand}'),
            'next': eval(f'lambda n: {iftrue} if n % {divitest} == 0 else {iffalse}'),
            'inspected': 0,
            'modulo': int(divitest)
        })
        for m_id, items_str, op, operand, divitest, iftrue, iffalse in re.findall(pattern, rawinpt)])
    )

def round(monkeys):
    ms = copy(monkeys)
    for i, monkey in enumerate(ms.values()):
        items = copy(monkey['items'])
        monkey['items'] = []
        for item_nr in items:
            new_worry_lvl = monkey['f'](item_nr) // 3
            ms[monkey['next'](new_worry_lvl)]['items'].append(new_worry_lvl)
            ms[i]['inspected'] += 1
    return ms

def first(monkeys):
    for _ in range(20):
        monkeys = round(monkeys)
    first, second, *_rest = sorted([(m['inspected'], i) for i, m in enumerate(monkeys.values())])[::-1]
    return first[0] * second[0]

def round2(monkeys, supermodulo):
    ms = copy(monkeys)
    for i, monkey in enumerate(ms.values()):
        items = copy(monkey['items'])
        monkey['items'] = []
        for item_nr in items:
            new_worry_lvl = monkey['f'](item_nr) % supermodulo
            ms[monkey['next'](new_worry_lvl)]['items'].append(new_worry_lvl)
            ms[i]['inspected'] += 1
    return ms

def second(monkeys):
    supermodulo = prod(m['modulo'] for m in monkeys.values())
    for _ in range(10000):
        monkeys = round2(monkeys, supermodulo)
    first, second, *_rest = sorted([(m['inspected'], i) for i, m in enumerate(monkeys.values())])[::-1]
    return first[0] * second[0]

example = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''