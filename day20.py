from tqdm import tqdm
from collections import deque

DAY = 20
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
    INPUT = list(map(int, RAW_INPUT.split('\n')[:-1]))

def sgn(n):
    if n > 0:  return 1
    if n < 0:  return -1
    if n == 0: return 0

def part1():
    length = len(INPUT)
    move_order = {i: num for i, num in enumerate(INPUT)}
    data = deque([(uid, num) for uid, num in enumerate(INPUT)])
    
    for i in range(length):
        shift_amount = move_order[i] % (length-1)
        data_point = (i, move_order[i])
        current_index = data.index(data_point)
        data.rotate(-current_index)
        value = data.popleft()
        data.insert(shift_amount, value)
        
    for zero_index, (_, num) in enumerate(data):
        if num == 0:
            break
    
    i1 = (zero_index + 1000) % length
    i2 = (zero_index + 2000) % length
    i3 = (zero_index + 3000) % length
    return data[i1][1] + data[i2][1] + data[i3][1]

def part2():
    length = len(INPUT)
    move_order = {i: num*811589153 for i, num in enumerate(INPUT)}
    data = deque([(uid, num*811589153) for uid, num in enumerate(INPUT)])
    
    for _ in range(10):
        for i in range(length):
            shift_amount = move_order[i] % (length-1)
            data_point = (i, move_order[i])
            current_index = data.index(data_point)
            data.rotate(-current_index)
            value = data.popleft()
            data.insert(shift_amount, value)
        
    for zero_index, (_, num) in enumerate(data):
        if num == 0:
            break
    
    i1 = (zero_index + 1000) % length
    i2 = (zero_index + 2000) % length
    i3 = (zero_index + 3000) % length
    return data[i1][1] + data[i2][1] + data[i3][1]

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
