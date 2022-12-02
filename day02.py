DAY = 2
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
        INPUT.append(line.split(' '))

# Each score is <move_value> + <outcome_value>.
# Both indices are moves here, so move_value doesn't 
# change between columns.
PART1_SCORES = {'A': {'X': 1 + 3, 'Y': 2 + 6, 'Z': 3 + 0},
                'B': {'X': 1 + 0, 'Y': 2 + 3, 'Z': 3 + 6},
                'C': {'X': 1 + 6, 'Y': 2 + 0, 'Z': 3 + 3}}

def part1():
    total_score = 0
    for opp_move, my_move in INPUT:
        total_score += PART1_SCORES[opp_move][my_move]
    return total_score

# Each score is <move_value> + <outcome_value>.
# The second index is outcome here, so outcome_value
# doesn't change between columns.
PART2_SCORES = {'A': {'X': 3 + 0, 'Y': 1 + 3, 'Z': 2 + 6},
                'B': {'X': 1 + 0, 'Y': 2 + 3, 'Z': 3 + 6},
                'C': {'X': 2 + 0, 'Y': 3 + 3, 'Z': 1 + 6}}

def part2():
    total_score = 0
    for opp_move, outcome in INPUT:
        total_score += PART2_SCORES[opp_move][outcome]
    return total_score
def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
