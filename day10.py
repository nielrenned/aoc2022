DAY = 10
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
    INPUT = []
    for line in RAW_INPUT.split('\n')[:-1]:
        INPUT.append(line.split())

def process_instructions():
    """Calculates the value of the X register during each clock cycle."""
    clock = 0
    X_values = [1]
    X = 1
    for instr in INPUT:
        op = instr[0]
        if op == 'noop':
            X_values.append(X)
            clock += 1
        elif op == 'addx':
            X_values.append(X)
            amount = int(instr[1])
            X += amount
            X_values.append(X)
            clock += 2

    return X_values

def part1():
    X_values = process_instructions()
    return sum(X_values[i-1] * i for i in range(20, 221, 40))

def part2():
    X_values = process_instructions()
    screen = [' ']*240

    for y in range(6):
        for x in range(40):
            clock = 40*y + x
            X = X_values[clock]
            if X-1 <= x <= X+1:
                screen[clock] = '#'
    
    ret_string = '\n'
    for y in range(6):
        for x in range(40):
            ret_string += screen[40*y+x] + ' '
        ret_string += '\n'
    
    return ret_string[:-1]

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
