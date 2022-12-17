DAY = 17
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
    for c in RAW_INPUT[:-1]:
        if c == '<':
            INPUT.append(-1)
        elif c == '>':
            INPUT.append(1)

# Bottom left of the bounding box will be (0,0) for the rock.
# This ordering will ensure rock[0] is a left-most point 
# and rock[-1] is a right-most point.
ROCKS = [
    [(0,0), (1,0), (2,0), (3,0)], # horizontal line
    [(0,1), (1,0), (1,1), (1,2), (2,1)], # plus
    [(0,0), (1,0), (2,0), (2,1), (2,2)], # L shape
    [(0,0), (0,1), (0,2), (0,3)], # vertical line
    [(0,0), (1,0), (0,1), (1,1)] # box shape
]

def try_move_rock_horizontal(rock, dx, chamber):
    for x,y in rock:
        if x+dx < 0 or x+dx > 6:
            return rock, False
        if 0 <= y < len(chamber) and chamber[y][x+dx] != '.':
            return rock, False
    
    return [(x + dx, y) for x,y in rock], True

def try_move_rock_vertical(rock, dy, chamber):
    for x,y in rock:
        if y+dy < 0:
            return rock, False
        if 0 <= y+dy < len(chamber) and chamber[y+dy][x] != '.':
            return rock, False
    
    return [(x, y + dy) for x,y in rock], True

def do_one_step(rock_index, chamber, jet_index, tower_height):
    # Spawn rock
    rock, _ = try_move_rock_vertical(ROCKS[rock_index % 5], tower_height + 3, chamber) # 3 units above current highest rock
    rock, _ = try_move_rock_horizontal(rock, 2, chamber) # 2 units away from left wall

    # Drop and jet rock
    while True:
        rock, _ = try_move_rock_horizontal(rock, INPUT[jet_index], chamber)
        jet_index += 1; jet_index %= len(INPUT)
        rock, did_fall = try_move_rock_vertical(rock, -1, chamber)
        if not did_fall:
            break
    
    # Add rock to chamber.
    rock_max_y = max(p[1] for p in rock)
    chamber.extend([['.']*7 for _ in range(0, rock_max_y - len(chamber) + 1)])
    for x,y in rock:
        tower_height = max(tower_height, y+1)
        chamber[y][x] = '#'
    
    return chamber, jet_index, tower_height

def part1():
    chamber = []
    tower_height = 0
    jet_index = 0
    for rock_index in range(2022):
        chamber, jet_index, tower_height = do_one_step(rock_index, chamber, jet_index, tower_height)
    
    return tower_height # This is equal to the tower height because rows are 0-indexed.


def part2():
    NUM_ROCKS = 1_000_000_000_000

    # Simulate until we find a repetition.
    # A repetition will be when the same rock is falling, the same jets are applying, and the top layer
    # of the chamber looks the same (not strictly true, but it works).
    chamber = []; tower_height = 0; jet_index = 0; rock_index = 0
    seen = {(rock_index, jet_index, tuple('.......')): rock_index}
    while True:
        chamber, jet_index, tower_height = do_one_step(rock_index, chamber, jet_index, tower_height)
        rock_index += 1

        if (rock_index % 5, jet_index, tuple(chamber[-1])) in seen: # We found a repetition
            break
        seen[(rock_index % 5, jet_index, tuple(chamber[-1]))] = rock_index

    initial_stack_height = tower_height
    initial_rock_count = rock_index

    # print(f'After {initial_rock_count} rocks the height is {initial_stack_height}.')

    # Check to see how repetition stacks (by doing another repetition)
    repetition_rock_count = rock_index - seen[(rock_index % 5, jet_index, tuple(chamber[-1]))]
    # print(f'The pattern repeats every {repetition_rock_count} rocks, starting at rock number {rock_index - repetition_rock_count}.')
    for _ in range(repetition_rock_count):
        chamber, jet_index, tower_height = do_one_step(rock_index, chamber, jet_index, tower_height)
        rock_index += 1
    
    each_repetition_adds = tower_height - initial_stack_height
    # print(f'Each repetition adds {each_repetition_adds} rocks.')

    # Calculate final stack rock count and height. We know
    #   initial_rock_count + n*repetition_rock_count + final_stack_rock_count == 1,000,000,000,000
    # with max n, so we can go (mod repetition_rock_count) to figure out the count.
    final_stack_rock_count = (NUM_ROCKS - initial_rock_count) % repetition_rock_count
    # print(f'To get to 1 trillion after all the repetitions, we need {final_stack_rock_count} more rocks.')
    temp = tower_height
    for _ in range(final_stack_rock_count):
        chamber, jet_index, tower_height = do_one_step(rock_index, chamber, jet_index, tower_height)
        rock_index += 1
    
    final_stack_height = tower_height - temp
    # print(f'These final rocks add {final_stack_height} height to the tower.')

    num_repetitions = (NUM_ROCKS - initial_rock_count - final_stack_rock_count) // repetition_rock_count
    # print(f'In between, we need {num_repetitions} more repetitions.')

    return initial_stack_height + num_repetitions * each_repetition_adds + final_stack_height

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
