import math
import time

DAY = 14
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
    wall_points = set()
    min_x, max_x, min_y, max_y = 500, 500, 0, 0
    for line in RAW_INPUT.split('\n')[:-1]:
        pairs = line.split(' -> ')
        for i in range(len(pairs)-1):
            p1 = tuple(map(int, pairs[i].split(',')))
            p2 = tuple(map(int, pairs[i+1].split(',')))
            for x,y in points_between_inclusive(p1, p2):
                wall_points.add((x,y))
                min_x = min(x, min_x)
                min_y = min(y, min_y)
                max_x = max(x, max_x)
                max_y = max(y, max_y)
    
    INPUT = (wall_points, (min_x, max_x, min_y, max_y))

def sgn(n):
    if n > 0:  return 1
    if n == 0: return 0
    if n < 0:  return -1

def points_between_inclusive(p1, p2):
    dx = p2[0] - p1[0]
    sx = sgn(dx)
    dy = p2[1] - p1[1]
    sy = sgn(dy)
    for i in range(max(abs(dx), abs(dy))+1):
        yield (p1[0] + i*sx, p1[1] + i*sy)

def part1():
    SAND_DIRECTIONS = [(0, 1), (-1, 1), (1, 1)] # order matters here!
    SAND_START = (500, 0)
    
    wall_points, (_, _, _, max_y) = INPUT
    sand_endpoints = set()
    
    # Start dropping sand!
    done_dropping = False
    while not (done_dropping):
        current_sand = SAND_START
        # Drop until it can't anymore or goes into the void
        while True:
            for dx, dy in SAND_DIRECTIONS:
                x, y = current_sand
                next_position = (x + dx, y + dy)
                if next_position not in sand_endpoints and next_position not in wall_points:
                    current_sand = next_position
                    break
            else:
                # If we get here, the sand can no longer move
                sand_endpoints.add(current_sand)
                break
            
            if current_sand[1] > max_y:
                done_dropping = True
                break
    
    return len(sand_endpoints)

def part2():
    SAND_DIRECTIONS = [(0, 1), (-1, 1), (1, 1)] # order matters here!
    SAND_START = (500, 0)
    
    wall_points, (_, _, _, max_y) = INPUT
    sand_endpoints = set()
    
    # Start dropping sand!
    while not (SAND_START in sand_endpoints):
        current_sand = SAND_START
        # Drop until it can't anymore or goes into the void
        while True:
            for dx, dy in SAND_DIRECTIONS:
                x, y = current_sand
                next_position = (x + dx, y + dy)
                if next_position not in sand_endpoints and next_position not in wall_points:
                    current_sand = next_position
                    break
            else:
                # If we get here, the sand can no longer move
                sand_endpoints.add(current_sand)
                break
            
            if current_sand[1] == max_y + 1:
                # If we get here, we reached the floor
                sand_endpoints.add(current_sand)
                break
    
    return len(sand_endpoints)

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
