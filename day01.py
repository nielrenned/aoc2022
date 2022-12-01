DAY = 1
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
    for line in RAW_INPUT.split('\n'):
        if line == '':
            INPUT.append(None)
        else:
            INPUT.append(int(line))

def part1():
    max_calories = 0
    total = 0
    for cals in INPUT:
        if cals is None:
            max_calories = max(total, max_calories)
            total = 0
        else:
            total += cals
    return max_calories

def part2():
    calorie_counts = []
    total = 0
    for cals in INPUT:
        if cals is None:
            calorie_counts.append(total)
            total = 0
        else:
            total += cals
    return sum(sorted(calorie_counts)[-3:])

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
