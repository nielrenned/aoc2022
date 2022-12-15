import portion

DAY = 15
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
        sensor_piece, beacon_piece = line.split(': ')
        
        sensor_x = int(sensor_piece[12:sensor_piece.index(',')])
        sensor_y = int(sensor_piece[sensor_piece.rindex('=')+1:])

        beacon_x = int(beacon_piece[23:beacon_piece.index(',')])
        beacon_y = int(beacon_piece[beacon_piece.rindex('=')+1:])

        INPUT.append(((sensor_x, sensor_y), (beacon_x, beacon_y)))

def md(p1, p2):
    '''Returns the manhattan distance between two points.'''
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def part1():
    ROW_Y = 2000000
    no_beacon_x_values = portion.empty()
    for ((sensor_x, sensor_y), (beacon_x, beacon_y)) in INPUT:
        beacon_dist = md((sensor_x, sensor_y), (beacon_x, beacon_y))

        if abs(sensor_y - ROW_Y) >= beacon_dist: # This sensor doesn't rule out any beacons
            continue

        x_wiggle_room = beacon_dist - abs(sensor_y - ROW_Y)
        no_beacon_x_values |= portion.closed(sensor_x - x_wiggle_room, sensor_x + x_wiggle_room)

    for ((_, _), (beacon_x, beacon_y)) in INPUT:
        if beacon_y == ROW_Y:
            no_beacon_x_values -= portion.singleton(beacon_x)
    
    # print(no_beacon_x_values)

    count = 0
    for interval in no_beacon_x_values:
        count += (interval.upper - interval.lower)
        if interval.left == portion.OPEN:
            count -= 1
        if interval.right == portion.OPEN:
            count -= 1

    return count


XY_BOUND = 4000000

from itertools import combinations

def part2():
    info = []
    for ((sensor_x, sensor_y), beacon) in INPUT:
        dist = md((sensor_x, sensor_y), beacon)
        info.append((sensor_x, sensor_y, dist))
    
    possible_points = set()

    # Look for 4 sensors that have a border point in common.
    for setof4 in combinations(info, 4):
        # Four sensors *could* have a border point in common if they are close enough.
        good_set = True
        for (s1x, s1y, d1), (s2x, s2y, d2) in combinations(setof4, 2):
            if md((s1x, s1y), (s2x, s2y)) > d1 + d2 + 2:
                good_set = False
                break
        
        if good_set:
            # Calculate the sixteen lines that make up the borders of the regions
            lines = [] # Stored as (m, b) for y = mx + b
            for sx, sy, d in setof4:
                lines.append((1, -sx+sy+(d+1)))
                lines.append((-1, sx+sy+(d+1)))
                lines.append((1, -sx+sy-(d+1)))
                lines.append((-1, sx+sy-(d+1)))
            
            # Look for intersections of perpendicular lines
            for (m1, b1), (m2, b2) in combinations(lines, 2):
                if m1 == m2:
                    continue
                x = (b2 - b1)/(m1 - m2)
                if int(x) != x:
                    continue
                x = int(x)
                y = m1*x + b1
                if 0 <= x <= XY_BOUND and 0 <= y <= XY_BOUND:
                    possible_points.add((x, y))

    for x, y in possible_points:
        for sx, sy, d in info:
            if md((x,y), (sx, sy)) <= d:
                break
        else:
            return 4000000*x + y



'''
from tqdm import tqdm
from multiprocessing import Pool
from itertools import starmap, repeat

def check_row(y):
    row_area = portion.empty()
    entire_row = portion.closed(0, XY_BOUND)
    for ((sensor_x, sensor_y), (beacon_x, beacon_y)) in INPUT:
        beacon_dist = md((sensor_x, sensor_y), (beacon_x, beacon_y))

        if abs(sensor_y - y) >= beacon_dist: # This sensor doesn't rule out any beacons in this row
            continue
        
        x_wiggle_room = beacon_dist - abs(sensor_y - y)
        row_area |= portion.open(sensor_x - x_wiggle_room - 1, sensor_x + x_wiggle_room + 1)
        if row_area.contains(entire_row):
            return -1
    
    open_area = entire_row - row_area # should be a singleton
    x = open_area.lower
    return 4000000*x + y

    
def init():
    load_input()
    parse_input()

def part2():
    with Pool(12, init, []) as p:
        for result in tqdm(p.imap_unordered(check_row, range(XY_BOUND+1), chunksize=1000), total=XY_BOUND+1):
            if result != -1:
                return result
'''

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()