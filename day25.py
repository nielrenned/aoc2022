import math

DAY = 25
RAW_INPUT = None
INPUT = None

def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/day{DAY}.txt'
    if use_test_input:
        path = f'inputs/day{DAY}_test.txt'
    with open(path) as f:
        RAW_INPUT = f.read()

def parse_input():
    global INPUT
    INPUT = RAW_INPUT.split('\n')[:-1]

def part1():
    lookup_table = {
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2': 2
    }
    
    total_fuel = 0
    for digit_str in INPUT:
        for i, digit in enumerate(digit_str[::-1]):
            total_fuel += lookup_table[digit] * 5**i
    
    normal_b5_digits = [0]
    highest_power = math.ceil(math.log(total_fuel, 5))
    for i in range(highest_power, -1, -1):
        next_digit = total_fuel // (5**i)
        normal_b5_digits.append(next_digit)
        total_fuel -= next_digit * (5**i)
    
    weird_b5_digits = normal_b5_digits[:]
    for i in range(len(weird_b5_digits)-1, -1, -1):
        if weird_b5_digits[i] <= 2: continue
        
        weird_b5_digits[i] -= 5
        weird_b5_digits[i-1] += 1
    
    start = 0
    while weird_b5_digits[start] == 0: start += 1
    
    weird_b5_str = ''
    for digit in weird_b5_digits[start:]:
        weird_b5_str += '012=-'[digit]
    
    return weird_b5_str

def part2():
    return "Merry Christmas!"

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()