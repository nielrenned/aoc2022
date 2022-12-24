from enum import IntEnum
from queue import SimpleQueue
from tqdm import tqdm

DAY = 24
RAW_INPUT = None
INPUT = None

def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/day{DAY:02}_test.txt'
    with open(path) as f:
        RAW_INPUT = f.read()

class Direction(IntEnum):
    UP = 0; DOWN = 1; LEFT = 2; RIGHT = 3

DELTAS  = [(0, -1), (0, 1), (-1, 0), (1, 0)]
DIR_STR = '^v<>'
DIRS    = [Direction(i) for i in range(4)]

def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return abs(x)

def lcm(x, y):
    return x*y // gcd(x, y)

def parse_input():
    global INPUT
    RAW_LINES = RAW_INPUT.split('\n')[:-1]
    
    blizzards = {Direction(i): set() for i in range(4)}
    for y, line in enumerate(RAW_LINES[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c != '.':
                dir_index = DIR_STR.index(c)
                blizzards[Direction(dir_index)].add((x,y))
    
    width = len(RAW_LINES[0]) - 2
    height = len(RAW_LINES) - 2
    
    blizzard_cycle = []
    for _ in range(lcm(width, height)):
        all_blizzards = blizzards[0] | blizzards[1] | blizzards[2] | blizzards[3]
        blizzard_cycle.append(all_blizzards)
        
        new_blizzards = {Direction(i): set() for i in range(4)}
        for dir in DIRS:
            for (bx, by) in blizzards[dir]:
                new_bx = (bx + DELTAS[dir][0]) % width
                new_by = (by + DELTAS[dir][1]) % height
                new_blizzards[dir].add((new_bx, new_by))
        
        blizzards = new_blizzards
    
    start_x = RAW_LINES[0].index('.') - 1
    end_x   = RAW_LINES[-1].index('.') - 1
    INPUT = ((width, height), (start_x, -1), (end_x, height), blizzard_cycle)

def shortest_path_length(sx, sy, st, ex, ey):
    (w, h), _, _, blizzard_cycle = INPUT
    num_cycles = lcm(w, h)
    
    possible_moves = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]
    
    q = SimpleQueue()
    q.put((sx, sy, st))
    seen = {(sx, sy, st)}
    while True:
        x, y, t = q.get()
        
        for dx, dy in possible_moves:
            new_x, new_y = x + dx, y + dy
            if new_x == ex and new_y == ey: return t + 1
            if not (
                (0 <= new_x < w and 0 <= new_y < h) or # We want to stay in the grid
                (new_x == sx and new_y == sy)          # We can also stay at the start
            ): continue
            
            blizzards = blizzard_cycle[(t+1) % num_cycles]
            
            if (new_x, new_y) not in blizzards:
                new_loc_time = (new_x, new_y, t+1)
                if new_loc_time not in seen:
                    seen.add(new_loc_time)
                    q.put(new_loc_time)

def part1():
    _, (start_x, start_y), (end_x, end_y), _ = INPUT
    return shortest_path_length(start_x, start_y, 0, end_x, end_y)

def part2():
    _, (start_x, start_y), (end_x, end_y), _ = INPUT
    t0 = shortest_path_length(start_x, start_y, 0,  end_x,   end_y)
    t1 = shortest_path_length(end_x,   end_y,   t0, start_x, start_y)
    t2 = shortest_path_length(start_x, start_y, t1, end_x,   end_y)
    return t2

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
