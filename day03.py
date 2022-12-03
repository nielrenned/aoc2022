import string

DAY = 3
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
    INPUT = RAW_INPUT.split('\n')[:-1]

PRIORITY = {x: i + 1 for i, x in enumerate(string.ascii_letters)}

def part1():
    total = 0
    for sack in INPUT:
        compartment1 = set(sack[:len(sack)//2])
        compartment2 = set(sack[len(sack)//2:])
        common_item = (compartment1 & compartment2).pop()
        total += PRIORITY[common_item]
    return total

def part2():
    total = 0
    for i in range(0, len(INPUT), 3):
        sack1, sack2, sack3 = map(set, INPUT[i:i+3])
        badge_item = (sack1 & sack2 & sack3).pop()
        total += PRIORITY[badge_item]
    return total

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
