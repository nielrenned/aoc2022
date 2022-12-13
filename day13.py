from enum import IntEnum
from copy import deepcopy
from functools import cmp_to_key

DAY = 13
RAW_INPUT = None
INPUT = None

def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/day{DAY:02}_test.txt'
    with open(path) as f:
        RAW_INPUT = f.read()

def parse_input():
    global INPUT
    RAW_LINES = RAW_INPUT.split('\n')
    INPUT = []
    for i in range(0, len(RAW_LINES), 3):
        left = eval(RAW_LINES[i])
        right = eval(RAW_LINES[i+1])
        INPUT.append((left, right))

class Order(IntEnum):
    CORRECT = -1
    INDETERMINATE = 0
    INCORRECT = 1

def compare(left, right):
    if type(left) == type(right) == int:
        if   left < right: return Order.CORRECT
        elif left > right: return Order.INCORRECT
        else             : return Order.INDETERMINATE
    
    if type(left) == type(right) == list:
        for i in range(min(len(left), len(right))):
            result = compare(left[i], right[i])
            if result != Order.INDETERMINATE:
                return result

        # If we get here, all comparisons were indeterminate
        if   len(left) < len(right): return Order.CORRECT
        elif len(left) > len(right): return Order.INCORRECT
        else                       : return Order.INDETERMINATE
    
    if type(left) == int and type(right) == list:
        return compare([left], right)
    if type(left) == list and type(right) == int:
        return compare(left, [right])

def part1():
    total = 0
    for i, (left, right) in enumerate(INPUT):
        if compare(left, right) == Order.CORRECT:
            total += i+1 # pairs are 1-indexed
    return total

def part2():
    packets = [[[2]], [[6]]]
    for left, right in INPUT:
        packets.append(left)
        packets.append(right)
    packets.sort(key=cmp_to_key(compare))
    return (packets.index([[2]])+1) * (packets.index([[6]])+1)

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
