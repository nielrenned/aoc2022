from collections import namedtuple
from copy import deepcopy

DAY = 5
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
    
    LINES = RAW_INPUT.split('\n')
    blank_index = LINES.index('')
    SETUP = LINES[:blank_index]
    INSTRUCTIONS = LINES[blank_index+1:-1]
    
    # Parsing initial stacks
    num_stacks = len(SETUP[-1].split())
    stacks = {i+1: [] for i in range(num_stacks)}
    for row in SETUP[:-1]:
        for i in range(0, len(row)//4 + 1):
            box_name = row[4*i + 1]
            if box_name != ' ':
                stacks[i+1].insert(0, box_name)
    
    # Parsing instructions
    Instruction = namedtuple('Instr', ['amount', 'from_stack', 'to_stack'])
    instructions = []
    for line in INSTRUCTIONS:
        pieces = line.split()
        instr = Instruction(int(pieces[1]), int(pieces[3]), int(pieces[5]))
        instructions.append(instr)
    
    INPUT = (stacks, instructions)

def part1():
    initial_stacks, instructions = INPUT
    stacks = deepcopy(initial_stacks)
    for (amount, from_stack, to_stack) in instructions:
        for _ in range(amount):
            stacks[to_stack].append(stacks[from_stack].pop())
    return ''.join(stacks[i][-1] for i in stacks)

def part2():
    initial_stacks, instructions = INPUT
    stacks = deepcopy(initial_stacks)
    for (amount, from_stack, to_stack) in instructions:
        stacks[to_stack] += stacks[from_stack][-amount:]
        stacks[from_stack] = stacks[from_stack][:-amount]
    return ''.join(stacks[i][-1] for i in stacks)

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
