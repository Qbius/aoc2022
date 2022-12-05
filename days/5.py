import re

def parse(rawinput):
    stacks_raw, instructions_raw = rawinput.split('\n\n')
    stacks = [list(e for e in stack if e != ' ') for stack in zip(*[list(line[1::2][::2]) for line in stacks_raw.split('\n')[:-1]])]
    instructions = [tuple(map(lambda n: int(n) - 1, re.match(r'move (\d+) from (\d+) to (\d+)', line).groups())) for line in instructions_raw.split('\n')]
    return stacks, instructions

def first(stacks, instructions):
    for count, frm, to in instructions:
        stacks[to][:0] = stacks[frm][count::-1]
        stacks[frm] = stacks[frm][count + 1:]
    return ''.join(first for first, *_rest in stacks)


def second(stacks, instructions):
    for count, frm, to in instructions:
        stacks[to][:0] = stacks[frm][:count + 1]
        stacks[frm] = stacks[frm][count + 1:]
    return ''.join(first for first, *_rest in stacks)

example = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2'''