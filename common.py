from re import search

class raw_input:
    pass

class RegexBase:
    pass

def regex(pattern, types):
    return type('', (RegexBase,), {'process': lambda lines: [[arg_type(arg) for arg, arg_type in zip(search(pattern, line).groups(), types)] for line in lines]})

class SingleLineBase:
    pass

def single_line(delimiter, typ):
    return type('', (SingleLineBase,), {'process': lambda raw_input: list(map(typ, raw_input.strip().split(delimiter)))})

class Pipe(object):
    map = lambda f: lambda l: list(map(f, l))
    filter = lambda f: lambda l: list(filter(f, l))

    def __init__(self, obj):
        self.obj = obj
        self.fs = []

    def __or__(self, callee):
        if callee is print:
            return self.obj
        else:
            self.obj = callee(self.obj)
            return self

P = Pipe

