from typing import get_type_hints
from common import RegexBase, SingleLineBase, raw_input
from os.path import exists, abspath
from datetime import datetime
import sys
import webbrowser
import requests

sys.path.insert(0, abspath('./days'))

if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    print('please specify the day')
    exit()

day = sys.argv[1]
example = any(arg in ['-e', '--example'] for arg in sys.argv)

inpt_path = f'inputs/{day}.txt'
year = datetime.now().year
if not exists(inpt_path):
    session = open('session.id').read().strip()
    inpt = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies={'session': session}, headers={'User-Agent': 'Mozilla/5.0'}).text.rstrip()
    with open(inpt_path, 'w') as o_file:
        o_file.write(inpt)

file_path = f'./days/{day}.py'
if not exists(file_path):
    template = '''
def first(values):
    pass

def second(values):
    pass
'''
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}')
    with open(file_path, 'w') as o_file:
        o_file.write(template)


day_module = __import__(day)

def parse_input(day_f, day_input_raw):
    day_input_lines = day_input_raw.split('\n')
    type_hints = list(get_type_hints(day_f).values())
    if not type_hints:
        return day_input_lines
    elif RegexBase in type_hints[0].__bases__:
        return type_hints[0].process(day_input_lines)
    elif SingleLineBase in type_hints[0].__bases__:
        return type_hints[0].process(day_input_raw)
    elif type_hints[0] == raw_input:
        return day_input_raw
    else:
        return list(map(type_hints[0], day_input_lines))

def call_with_appropriate_arg(day_f):
    day_input_raw = (day_module.example if example else open(f'inputs/{day}.txt').read()).rstrip().replace('\r\n', '\n')
    parsed_input = day_module.parse(day_input_raw) if hasattr(day_module, 'parse') else parse_input(day_f, day_input_raw)
    return day_f(*parsed_input) if isinstance(parsed_input, tuple) else day_f(parsed_input)


notimpl = lambda *_: 'not implemented'
day_first = getattr(day_module, 'first', notimpl)
day_second = getattr(day_module, 'second', notimpl)
day_extra = getattr(day_module, 'extra', notimpl)

print('First:', call_with_appropriate_arg(day_first))
print('Second:', call_with_appropriate_arg(day_second))
if not example and day_extra != notimpl:
    call_with_appropriate_arg(day_extra)