from common import raw_input

def first(buffer: raw_input, length=4):
    return next(i for i in range(length, len(buffer) + 1) if len(set(buffer[i - length:i])) == length)

def second(buffer: raw_input):
    return first(buffer, length=14)

example = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'