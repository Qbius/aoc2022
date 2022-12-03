
from pandas import Series

letters = list(map(chr, range(ord('a'), ord('z') + 1))) + list(map(chr, range(ord('A'), ord('Z') + 1)))
def priority(letter):
    return letters.index(letter) + 1

def first(values):
    return sum(sum(map(priority, set(row[:len(row) // 2]) & set(row[len(row) // 2:]))) for row in values)

def second(values):
    return sum(sum(map(priority, set(values[i]) & set(values[i + 1]) & set(values[i + 2]))) for i in range(0, len(values), 3))

example = '''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''