from typing import Callable

DAY = 11
RAW_INPUT = None
INPUT = None

def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/day{DAY:02}_test.txt'
    with open(path) as f:
        RAW_INPUT = f.read()

class Monkey:
    def __init__(self, 
                 starting_items: list, 
                 operation_pieces: list, 
                 modulus: int, 
                 next_monkey_id_if_true: int, 
                 next_monkey_id_if_false: int):
        
        self.inspection_count = 0
        self.starting_items = starting_items
        self.items = starting_items[:]
        self.modulus = modulus
        self.next_monkey_id_if_true = next_monkey_id_if_true
        self.next_monkey_id_if_false = next_monkey_id_if_false

        left, op_char, right = operation_pieces
        if left.isnumeric():  left = int(left)
        if right.isnumeric(): right = int(right)
        
        if op_char == '+':   op = int.__add__
        elif op_char == '*': op = int.__mul__
        
        self.op_left = left
        self.op_right = right
        self.op = op
    
    def next_monkey_id(self, item_value):
        if item_value % self.modulus == 0:
            return self.next_monkey_id_if_true
        else:
            return self.next_monkey_id_if_false
    
    def do_operation(self, item_value):
        left_value  = item_value if self.op_left == 'old'  else self.op_left
        right_value = item_value if self.op_right == 'old' else self.op_right
        return self.op(left_value, right_value)
    
    def reset(self):
        self.items = self.starting_items[:]
        self.inspection_count = 0

def parse_input():
    global INPUT
    RAW_LINES = RAW_INPUT.split('\n')
    INPUT = []
    for i in range(0, len(RAW_LINES), 7):
        items_list = list(map(int, RAW_LINES[i+1].split(': ')[-1].split(', ')))
        operation_pieces = RAW_LINES[i+2].split(' = ')[-1].split(' ')
        test_modulus = int(RAW_LINES[i+3].split(' ')[-1])
        next_monkey_id_if_true = int(RAW_LINES[i+4].split(' ')[-1])
        next_monkey_id_if_false = int(RAW_LINES[i+5].split(' ')[-1])

        monkey = Monkey(items_list, operation_pieces, test_modulus, 
                        next_monkey_id_if_true, next_monkey_id_if_false)
        INPUT.append(monkey)

def part1():
    for _ in range(20):
        for monkey in INPUT:
            for item_value in monkey.items:
                monkey.inspection_count += 1
                new_value = monkey.do_operation(item_value) // 3
                next_monkey = INPUT[monkey.next_monkey_id(new_value)]
                next_monkey.items.append(new_value)
            monkey.items.clear() # The monkey has thrown all its items.
    
    sorted_monkeys = sorted(INPUT, key=lambda m: m.inspection_count)
    return sorted_monkeys[-1].inspection_count * sorted_monkeys[-2].inspection_count

def part2():
    moduli_product = 1
    for monkey in INPUT:
        monkey.reset() # In Part 1, we modify the monkeys, so we have to reset them.
        moduli_product *= monkey.modulus

    for _ in range(10000):
        for monkey in INPUT:
            for item_value in monkey.items:
                monkey.inspection_count += 1
                new_value = monkey.do_operation(item_value)
                next_monkey = INPUT[monkey.next_monkey_id(new_value)]
                next_monkey.items.append(new_value % moduli_product)
            monkey.items.clear() # The monkey has thrown all its items.

    sorted_monkeys = sorted(INPUT, key=lambda m: m.inspection_count)
    return sorted_monkeys[-1].inspection_count * sorted_monkeys[-2].inspection_count

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
