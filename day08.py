DAY = 8
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
        INPUT.append(list(map(int, line)))

# Note: modifies the visible list
def update_visible(x: int, y: int, highest_seen: int, visible: list):
    tree_height = INPUT[y][x]
    if tree_height > highest_seen:
        visible[y][x] = True
        highest_seen = tree_height
    return highest_seen

def part1():
    width = len(INPUT[0])
    height = len(INPUT)
    visible = [[False for _ in range(width)] for _ in range(height)]

    # Rows
    for y in range(height):
        # Moving Right
        highest_seen = -1
        for x in range(width):
            highest_seen = update_visible(x, y, highest_seen, visible)
        
        # Moving Left
        highest_seen = -1
        for x in range(width-1, -1, -1):
            highest_seen = update_visible(x, y, highest_seen, visible)
    
    # Columns
    for x in range(width):
        # Moving Down
        highest_seen = -1
        for y in range(height):
            highest_seen = update_visible(x, y, highest_seen, visible)
        
        # Moving Up
        highest_seen = -1
        for y in range(height-1, -1, -1):
            highest_seen = update_visible(x, y, highest_seen, visible)

    count = 0
    for row in visible:
        for tree_visible in row:
            if tree_visible:
                count += 1
    
    return count

def count_visible(x0: int, y0: int, dx: int, dy: int):
    width = len(INPUT[0])
    height = len(INPUT)
    starting_height = INPUT[y0][x0]

    x, y = x0+dx, y0+dy
    count = 0
    while 0 <= x < width and 0 <= y < height:
        if INPUT[y][x] < starting_height:
            count += 1
        if INPUT[y][x] >= starting_height: # We can also see the last tree!
            count += 1
            break
        x += dx
        y += dy
    
    return count

def part2():
    width = len(INPUT[0])
    height = len(INPUT)
    directions = [(1,0), (0,1), (-1,0), (0,-1)]
    best_score = 0
    for x in range(width):
        for y in range(height):
            score = 1
            for dx, dy in directions:
                score *= count_visible(x, y, dx, dy)
            best_score = max(score, best_score)
    return best_score

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
