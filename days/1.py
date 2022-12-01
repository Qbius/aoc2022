from common import raw_input

def get_elfs(rawinpt):
    return [list(map(int, elf.split('\n'))) for elf in rawinpt.split('\n\n')]

def first(rawinpt: raw_input):
    return max(map(sum, get_elfs(rawinpt)))

def second(rawinpt: raw_input):
    top1, top2, top3, *_rest = sorted(map(sum, get_elfs(rawinpt)))[::-1]
    return top1 + top2 + top3
