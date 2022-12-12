from queue import SimpleQueue

DAY = 12
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
    altitudes = []
    start_pos = None
    end_pos = None
    for y, line in enumerate(RAW_INPUT.split('\n')[:-1]):
        row = []
        for x, c in enumerate(line):
            if c == 'S':
                start_pos = (x, y)
                height = 0
            elif c == 'E':
                end_pos = (x,y)
                height = 25
            else:
                height = ord(c) - ord('a')
            row.append(height)
        altitudes.append(row)
    INPUT = (start_pos, end_pos, altitudes)

def shortest_path(start_pos, end_pos):
    _, _, altitudes = INPUT
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    map_height = len(altitudes)
    map_width = len(altitudes[0])

    node_queue = SimpleQueue()
    node_queue.put((start_pos, 0))
    visited = {start_pos}

    while not node_queue.empty():
        current_pos, current_path_length = node_queue.get()
        x, y = current_pos
        current_altitude = altitudes[y][x]

        for dx, dy in directions:
            next_x = x + dx
            next_y = y + dy

            if (
                not (0 <= next_x < map_width and 0 <= next_y < map_height) or
                (next_x, next_y) in visited or
                altitudes[next_y][next_x] > current_altitude + 1
            ):
                continue
            
            if (next_x, next_y) == end_pos:
                return current_path_length + 1
            
            visited.add((next_x, next_y))
            node_queue.put(((next_x, next_y), current_path_length + 1))

def part1():
    start_pos, end_pos, _ = INPUT
    return shortest_path(start_pos, end_pos)

def part2():
    _, end_pos, altitudes = INPUT

    min_length = 100000
    for y, row in enumerate(altitudes):
        for x, altitude in enumerate(row):
            if altitude != 0: continue

            path_length = shortest_path((x, y), end_pos)
            if path_length is not None:
                min_length = min(min_length, path_length)
    
    return min_length

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
