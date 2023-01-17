DAY = 22
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
    
    # Build map
    map = []
    max_length = 0
    for line in RAW_LINES[:-2]:
        max_length = max(max_length, len(line))
        map.append(line)
    
    for i, line in enumerate(map):
        map[i] = line + ' '*(max_length - len(line))
    
    # Break up instructions
    INSTR_LINE = RAW_LINES[-1]
    instructions = []
    s = ''
    i = 0
    while i < len(INSTR_LINE):
        c = INSTR_LINE[i]
        if c.isalpha():
            instructions.append(int(s))
            instructions.append(c)
            s = ''
        else:
            s += c
        i += 1
    
    if s != '':
        instructions.append(int(s))
    
    INPUT = (instructions, map)

RIGHT = 0
DOWN  = 1
LEFT  = 2
UP    = 3

DELTAS = [(1,0), (0,1), (-1,0), (0,-1)]

def part1():
    instructions, map = INPUT
    
    dir = RIGHT
    
    # Find the starting point
    y = 0
    for x in range(len(map[y])):
        if map[y][x] == '.':
            break
    
    # Do the walk
    for instr in instructions:
        if instr == 'R':
            dir += 1; dir %= 4
            continue
        if instr == 'L':
            dir -= 1; dir %= 4
            continue
        
        # If we get here, we know we have a number of steps.
        # Walk in current direction until we have to stop.
        dx, dy = DELTAS[dir]
        for _ in range(instr):
            # Get next location
            new_x, new_y = (x + dx) % len(map[0]), (y + dy) % len(map)
            while map[new_y][new_x] == ' ':
                new_x, new_y = (new_x + dx) % len(map[0]), (new_y + dy) % len(map)
            
            if map[new_y][new_x] == '#':
                break
            
            x, y = new_x, new_y
    
    return (y+1)*1000 + (x+1)*4 + dir

WEST  = 0 # Coming from the west,  you move RIGHT = 0
NORTH = 1 # Coming from the north, you move DOWN  = 1
EAST  = 2 # Coming from the east,  you move LEFT  = 2
SOUTH = 3 # Coming from the south, you move UP    = 3

def outer_edge_points(region_top_lefts, region, edge):
    x0, y0 = region_top_lefts[region]
    if edge == NORTH: return (x0,  y0 - 1),  (x0 + 49, y0 - 1)
    if edge == SOUTH: return (x0,  y0 + 50), (x0 + 49, y0 + 50)
    if edge == EAST:  return (x0 + 50, y0),  (x0 + 50, y0 + 49)
    if edge == WEST:  return (x0 - 1,  y0),  (x0 - 1,  y0 + 49)

def inner_edge_points(region_top_lefts, region, edge):
    x0, y0 = region_top_lefts[region]
    if edge == NORTH: return (x0,      y0),      (x0 + 49, y0)
    if edge == SOUTH: return (x0,      y0 + 49), (x0 + 49, y0 + 49)
    if edge == EAST:  return (x0 + 49, y0),      (x0 + 49, y0 + 49)
    if edge == WEST:  return (x0,      y0),      (x0,      y0 + 49)

def edge_transit(region_top_lefts, edge_gluings, from_region, from_edge, point):
    to_region, to_edge, reverse_orientation = edge_gluings[from_region][from_edge]
    
    # How far along the line are we?
    x, y = point
    (x0, y0), (x1, y1) = outer_edge_points(region_top_lefts, from_region, from_edge)
    if y0 == y1: steps = x - x0
    else:        steps = y - y0
    
    # Go that far along the other line
    (x0, y0), (x1, y1) = inner_edge_points(region_top_lefts, to_region, to_edge)
    if reverse_orientation:
        (x0, y0), (x1, y1) = (x1, y1), (x0, y0)
    
    new_x, new_y = x0 + steps*(x1 - x0)//49, y0 + steps*(y1 - y0)//49
    return new_x, new_y

def get_region_from_location(region_top_lefts, x, y):
    for region in region_top_lefts:
        x0, y0 = region_top_lefts[region]
        if 0 <= (x - x0) < 50 and 0 <= (y - y0) < 50: return region
    return -1 # Off the map

def part2():
    instructions, map = INPUT
        
    # My cube net looks like this:
    #    2 1
    #    3
    #  5 4
    #  6 
    
    region_top_lefts = {
        1: (100, 0),
        2: (50, 0),
        3: (50, 50),
        4: (50, 100),
        5: (0, 100),
        6: (0, 150)
    }
    
    # edge_gluings[face][edge] = (new_face, new_edge, reverse_orientation)
    # 
    # In the functions that give the endpoints, they are returned from 
    # left-to-right or top-to-bottom in map orientation. In this data,
    # `reverse_orientation` will be true if, with respect to this ordering,
    # the *opposite* corners need to be glued.
    edge_gluings = {
        1: {NORTH: (6, SOUTH, False),
            SOUTH: (3, EAST,  False),
            EAST:  (4, EAST,  True),
            WEST:  (2, EAST,  False)},
        2: {NORTH: (6, WEST,  False),
            SOUTH: (3, NORTH, False),
            EAST:  (1, WEST,  False),
            WEST:  (5, WEST,  True)},
        3: {NORTH: (2, SOUTH, False),
            SOUTH: (4, NORTH, False),
            EAST:  (1, SOUTH, False),
            WEST:  (5, NORTH, False)},
        4: {NORTH: (3, SOUTH, False),
            SOUTH: (6, EAST,  False),
            EAST:  (1, EAST,  True),
            WEST:  (5, EAST,  False)},
        5: {NORTH: (3, WEST,  False),
            SOUTH: (6, NORTH, False),
            EAST:  (4, WEST,  False),
            WEST:  (2, WEST,  True)},
        6: {NORTH: (5, SOUTH, False),
            SOUTH: (1, NORTH, False),
            EAST:  (4, SOUTH, False),
            WEST:  (2, NORTH, False)}
    }
    
    # Find the starting point
    y = 0
    for x in range(len(map[y])):
        if map[y][x] == '.':
            break
    
    current_region = get_region_from_location(region_top_lefts, x, y)
    dir = RIGHT
    
    # Do the walk
    for instr in instructions:
        if instr == 'R':
            dir += 1; dir %= 4
            continue
        if instr == 'L':
            dir -= 1; dir %= 4
            continue
        
        # If we get here, we know we have a number of steps.
        # Walk in current direction until we have to stop.
        for _ in range(instr):
            dx, dy = DELTAS[dir]
            new_x, new_y = x + dx, y + dy
            new_dir = dir
            next_region = get_region_from_location(region_top_lefts, new_x, new_y)
            
            if next_region != current_region:
                if dir == LEFT:  edge = WEST
                if dir == RIGHT: edge = EAST
                if dir == UP:    edge = NORTH
                if dir == DOWN:  edge = SOUTH
                new_x, new_y = edge_transit(region_top_lefts, edge_gluings, current_region, edge, (new_x, new_y))
                new_dir = edge_gluings[current_region][edge][1]
            
            if map[new_y][new_x] == '#':
                break
            
            x, y = new_x, new_y
            dir = new_dir
            current_region = get_region_from_location(region_top_lefts, x, y)
    
    return (y+1)*1000 + (x+1)*4 + dir

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
