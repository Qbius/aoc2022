from common import raw_input
from itertools import starmap
from iteration_utilities import starfilter
from functools import cmp_to_key

def compare(a, b):
    if type(a) != type(b):
        a = [a] if isinstance(a, int) else a
        b = [b] if isinstance(b, int) else b
    
    if isinstance(a, int):
        return a - b
    else:
        list_comparison = next((res for res in starmap(compare, zip(a, b)) if res != 0), 0)
        return list_comparison or len(a) - len(b)
     
def first(rawinpt: raw_input):
    pairs = [tuple(map(eval, pair.split('\n'))) for pair in rawinpt.split('\n\n')]
    return sum(i + 1 for i, pair in starfilter(lambda i, pair: compare(*pair) == 1, enumerate(pairs)))

def second(lines):
    div1 = [[2]]
    div2 = [[6]]
    packets = sorted([div1, div2, *list(map(eval, filter(len, lines)))], key=cmp_to_key(compare))
    return (packets.index(div1) + 1) * (packets.index(div2) + 1)
    

example = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''