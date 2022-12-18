from queue import SimpleQueue

DAY = 18
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
    INPUT = set()
    for line in RAW_INPUT.split('\n')[:-1]:
        location = tuple(map(int, line.split(',')))
        INPUT.add(location)

def adjacent_locations(cube_loc):
    directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    for dx, dy, dz in directions:
        yield (cube_loc[0] + dx, cube_loc[1] + dy, cube_loc[2] + dz)

def part1():
    total = 0
    for cube_loc in INPUT:
        for adjacent_loc in adjacent_locations(cube_loc):
            if adjacent_loc not in INPUT:
                total += 1
    return total

def part2():
    bounds = [0,0,0]
    for x, y, z in INPUT:
        bounds[0] = max(x+1, bounds[0])
        bounds[1] = max(y+1, bounds[1])
        bounds[2] = max(z+1, bounds[2])
    
    q = SimpleQueue()
    q.put(tuple(bounds))
    explored = set()
    total = 0
    while not q.empty():
        loc = q.get()
        if loc in explored: continue

        explored.add(loc)
        for adj_loc in adjacent_locations(loc):
            if adj_loc in INPUT:
                total += 1
            elif (
                adj_loc not in explored and 
                -1 <= adj_loc[0] <= bounds[0] and
                -1 <= adj_loc[1] <= bounds[1] and
                -1 <= adj_loc[2] <= bounds[2]
            ):
                q.put(adj_loc)
    return total

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
