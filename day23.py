from collections import defaultdict, deque
from copy import copy

DAY = 23
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
    RAW_LINES = RAW_INPUT.split('\n')[:-1]
    INPUT = set()
    for y, line in enumerate(RAW_LINES):
        for x, c in enumerate(line):
            if c == '#':
                INPUT.add((x,y))

# Short for points-sum
def psum(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

EIGHT_DIRS = [(dx, dy) for dx in [-1,0,1] for dy in [-1,0,1] if (dx, dy) != (0, 0)]

def elf_wants_to_move(elf_loc, elves):
    for delta in EIGHT_DIRS:
        if psum(elf_loc, delta) in elves:
            return True
    return False

def elf_proposed_location(elf_loc, elf_locations, check_order):
    for delta0, delta1, delta2 in check_order:
        if (
            psum(elf_loc, delta0) not in elf_locations and
            psum(elf_loc, delta1) not in elf_locations and
            psum(elf_loc, delta2) not in elf_locations
        ):
            return psum(elf_loc, delta0)
    return elf_loc

def move_elves(elf_locations, check_order):
    num_elves_moved = 0
    next_locations = set()
    proposed_locations = dict()
    location_counts = defaultdict(int)
    
    for elf_loc in elf_locations:
        if not elf_wants_to_move(elf_loc, elf_locations):
            next_locations.add(elf_loc)
            continue
        
        next_loc = elf_proposed_location(elf_loc, elf_locations, check_order)
        proposed_locations[elf_loc] = next_loc
        location_counts[next_loc] += 1
    
    for elf_loc in proposed_locations:
        next_loc = proposed_locations[elf_loc]
        if location_counts[next_loc] == 1:
            next_locations.add(next_loc)
            num_elves_moved += 1
        else:
            next_locations.add(elf_loc)
    
    return next_locations, num_elves_moved

def part1():
    check_order = deque([((0, -1), (-1, -1), (1, -1)),   # N, NW, NE
                         ((0, 1),  (-1, 1),  (1, 1)),    # S, SW, SE
                         ((-1, 0), (-1, -1), (-1, 1)),   # W, NW, SW
                         ((1, 0),  (1, -1),  (1, 1))])   # E, NE, SE
    
    elf_locations = INPUT
    for _ in range(10):
        elf_locations, _ = move_elves(elf_locations, check_order)
        check_order.rotate(-1)
    
    min_x = min(elf_loc[0] for elf_loc in elf_locations)
    max_x = max(elf_loc[0] for elf_loc in elf_locations)
    min_y = min(elf_loc[1] for elf_loc in elf_locations)
    max_y = max(elf_loc[1] for elf_loc in elf_locations)
    
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(INPUT)

def part2():
    check_order = deque([((0, -1), (-1, -1), (1, -1)),   # N, NW, NE
                         ((0, 1),  (-1, 1),  (1, 1)),    # S, SW, SE
                         ((-1, 0), (-1, -1), (-1, 1)),   # W, NW, SW
                         ((1, 0),  (1, -1),  (1, 1))])   # E, NE, SE
    
    elf_locations = INPUT
    round = 1
    while True:
        elf_locations, num_elves_moved = move_elves(elf_locations, check_order)
        if num_elves_moved == 0:
            return round
        check_order.rotate(-1)
        round += 1

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
