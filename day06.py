DAY = 6
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
    INPUT = list(RAW_INPUT[:-1])

def part1():
    for i in range(3, len(INPUT)):
        if len(set(INPUT[i-3:i+1])) == 4:
            return i+1

def part2():
    for i in range(13, len(INPUT)):
        if len(set(INPUT[i-13:i+1])) == 14:
            return i+1

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
