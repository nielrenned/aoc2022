DAY = 4
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
        s1, s2 = line.split(',')
        s1_start, s1_end = map(int, s1.split('-'))
        s2_start, s2_end = map(int, s2.split('-'))
        INPUT.append(((s1_start, s1_end), (s2_start, s2_end)))

def part1():
    count = 0
    for (s1_start, s1_end), (s2_start, s2_end) in INPUT:
        if s1_start <= s2_start and s2_end <= s1_end or \
           s2_start <= s1_start and s1_end <= s2_end:
            count += 1
    return count

def part2():
    count = 0
    for (s1_start, s1_end), (s2_start, s2_end) in INPUT:
        if s1_start <= s2_start and s2_start <= s1_end or \
           s2_start <= s1_start and s1_start <= s2_end:
            count += 1
    return count

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
