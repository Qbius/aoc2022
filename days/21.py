from functools import reduce
import re

def parse(lines):
    return dict(line.replace('/', '//').split(': ') for line in lines)

def expand(monkeys, monkeycode):
    def subit(monkeyv):
        return f'''({reduce(lambda acc, code: acc.replace(code, subit(monkeys[code])), re.findall(r'(^[a-z]{4}|[a-z]{4}$)', monkeyv), monkeyv)})'''
    
    return subit(monkeys[monkeycode])
def first(monkeys):
    return eval(expand(monkeys, 'root'))

class Variable(object):
    def __init__(self):
        self.operations = []

    def __add__(self, n):
        self.operations.append(lambda a: a - n)
        return self

    def __radd__(self, n):
        self.operations.append(lambda a: a - n)
        return self

    def __mul__(self, n):
        self.operations.append(lambda a: a // n)
        return self

    def __rmul__(self, n):
        self.operations.append(lambda a: a // n)
        return self

    def __sub__(self, n):
        self.operations.append(lambda a: a + n)
        return self

    def __rsub__(self, n):
        self.operations.append(lambda a: n - a)
        return self

    def __floordiv__(self, n):
        self.operations.append(lambda a: a * n)
        return self

    def __rfloordiv__(self, n):
        self.operations.append(lambda a: n // a)
        return self

    def equals(self, a):
        return reduce(lambda acc, operation: operation(acc), self.operations[::-1], a)
   
def second(monkeys):
    monkeys['humn'] = 'Variable()'
    cons1, cons2 = expand(monkeys, monkeys['root'][:4]), expand(monkeys, monkeys['root'][-4:])
    var = eval(expand(monkeys, monkeys['root'][:4]), globals(), locals())
    num = eval(expand(monkeys, monkeys['root'][-4:]))
    return var.equals(num)

example = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''