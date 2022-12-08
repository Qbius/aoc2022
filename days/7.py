from common import regex, raw_input
from functools import reduce

def crawl(tape):
    filesystem = {'/': {}}
    root = ''
    for info, val in tape:
        path = reduce(lambda d, segment: d[segment], [seg for seg in root.split('/') if seg], filesystem['/'])
        match info:
            case 'cd':
                root = '' if val == '/' else '/'.join(root.split('/')[:-1]) if val == '..' else f'{root}/{val}'
            case 'dir':
                path[val] = {}
            case '$':
                pass
            case _:
                path[val] = int(info)
    return filesystem

def get_size_listing(filesystem):
    size_listing = []
    def inner(info):
        if isinstance(info, int):
            return info
        else:
            nonlocal size_listing
            size = sum(map(inner, info.values()))
            size_listing.append(size)
            return size
    inner(filesystem['/'])
    return size_listing

def first(values: regex(r'(?:\$ |)([a-z0-9$]+) ([a-z\.\/]+)', [str, str])):    
    filesystem = crawl(values)
    sizes = get_size_listing(filesystem)
    return sum(v for v in sizes if v <= 100000)

def second(values: regex(r'(?:\$ |)([a-z0-9$]+) ([a-z\.\/]+)', [str, str])):
    filesystem = crawl(values)
    sizes = get_size_listing(filesystem)
    remaining_space = max(sizes) - 40000000
    return min(v for v in sizes if v >= remaining_space)

example = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''