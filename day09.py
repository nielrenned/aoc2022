DAY = 9
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
        dir, amount = line.split()
        INPUT.append((dir, int(amount)))

def get_new_location(head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail
    dx, dy = head_x - tail_x, head_y - tail_y
    if abs(dx) == 2:
        tail_x += dx//2
        if abs(dy) == 1:
            tail_y += dy
    if abs(dy) == 2:
        tail_y += dy//2
        if abs(dx) == 1:
            tail_x += dx
    return tail_x, tail_y

def part1():
    head_x, head_y = 0, 0
    tail_x, tail_y = 0, 0
    tail_locations = {(0,0)}
    directions = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}

    for dir, amount in INPUT:
        move_x, move_y = directions[dir]
        for _ in range(amount):
            # Update head loc
            head_x += move_x
            head_y += move_y

            # Update tail loc
            tail_x, tail_y = get_new_location((head_x, head_y), (tail_x, tail_y))
            tail_locations.add((tail_x, tail_y))

    return len(tail_locations)

def part2():
    locations = [(0,0) for _ in range(10)]
    tail_locations = {(0,0)}
    directions = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}

    for dir, amount in INPUT:
        move_x, move_y = directions[dir]
        for _ in range(amount):
            # Update head
            head_x, head_y = locations[0]
            locations[0] = (head_x + move_x, head_y + move_y)
            
            # Update tails
            for i in range(1, 10):
                locations[i] = get_new_location(locations[i-1], locations[i])
            
            tail_locations.add(locations[-1])
    
    return len(tail_locations)

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
