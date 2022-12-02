from common import regex
from pandas import Series

def first(values: regex(r'([A-C]) ([X-Z])', [str, str])):
    opponent, me = tuple(map(Series, zip(*values)))
    opponent = opponent.apply(ord) - ord('A')
    me = me.apply(ord) - ord('X')
    return sum((me + 1) + ((((me - opponent) + 1) % 3) * 3))

def second(values: regex(r'([A-C]) ([X-Z])', [str, str])):
    opponent, me = tuple(map(Series, zip(*values)))
    opponent = opponent.apply(ord) - ord('A')
    me = me.apply(ord) - ord('X')
    return sum((((opponent + me - 1) % 3) + 1) + me * 3)

example = '''
A Y
B X
C Z'''
