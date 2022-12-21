from copy import copy
from fractions import Fraction

DAY = 21
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
    INPUT = dict()
    
    for line in RAW_INPUT.split('\n')[:-1]:
        monkey, output = line.split(': ')
        if output.isnumeric():
            INPUT[monkey] = int(output)
        else:
            left, op, right = output.split(' ')
            INPUT[monkey] = (left, op, right)

def part1():
    monkeys = copy(INPUT)
    
    all_done = False
    while not all_done:
        all_done = True
        for monkey in monkeys:
            output = monkeys[monkey]
            if type(output) == int: continue
            
            left, op, right = output
            lvalue = monkeys[left]
            rvalue = monkeys[right]
            if type(lvalue) == tuple or type(rvalue) == tuple: all_done = False
            elif op == '+': monkeys[monkey] = lvalue + rvalue
            elif op == '-': monkeys[monkey] = lvalue - rvalue
            elif op == '*': monkeys[monkey] = lvalue * rvalue
            elif op == '/': monkeys[monkey] = lvalue // rvalue
    
    return monkeys['root']

# Representation of ax+b
class LinearExpression:
    def __init__(self, a, b):
        self.a = Fraction(a)
        self.b = Fraction(b)
    
    def __add__(self, other):
        if type(other) != LinearExpression:
            raise ValueError(f'Whoops: ({self}) + ({other})')
        return LinearExpression(self.a + other.a, self.b + other.b)
    
    def __sub__(self, other):
        if type(other) != LinearExpression:
            raise ValueError(f'Whoops: ({self}) - ({other})')
        return LinearExpression(self.a - other.a, self.b - other.b)
    
    def __mul__(self, other):
        if type(other) != LinearExpression or (self.a != 0 and other.a != 0):
            raise ValueError(f'Whoops: ({self}) * ({other})')
        if self.a != 0:
            return LinearExpression(self.a * other.b, self.b * other.b)
        if self.a == 0:
            return LinearExpression(other.a * self.b, other.b * self.b)
    
    def __truediv__(self, other):
        if type(other) != LinearExpression or other.a != 0: 
            raise ValueError(f'Whoops: ({self}) / ({other})')
        return LinearExpression(self.a / other.b, self.b / other.b)
    
    def __repr__(self) -> str:
        if self.a == 0:
            return f'{self.b}'
        if self.b == 0:
            return f'{self.a}*x'
        if self.b < 0:
            return f'{self.a}*x - {-self.b}'
        return f'{self.a}*x + {self.b}'

def part2():
    monkeys = dict()
    
    for monkey in INPUT:
        if monkey == 'root': continue
        if type(INPUT[monkey]) == int:
            monkeys[monkey] = LinearExpression(0, INPUT[monkey])
        else:
            monkeys[monkey] = INPUT[monkey]
    
    monkeys['humn'] = LinearExpression(1, 0)
    
    all_done = False
    while not all_done:
        all_done = True
        for monkey in monkeys:
            output = monkeys[monkey]
            if type(output) == LinearExpression: continue
            
            left, op, right = output
            lvalue = monkeys[left]
            rvalue = monkeys[right]
            if type(lvalue) == tuple or type(rvalue) == tuple: all_done = False
            elif op == '+': monkeys[monkey] = lvalue + rvalue
            elif op == '-': monkeys[monkey] = lvalue - rvalue
            elif op == '*': monkeys[monkey] = lvalue * rvalue
            elif op == '/': monkeys[monkey] = lvalue / rvalue
    
    # Solution to ax+b = cx+d is x = (d-b)/(a-c)
    root = INPUT['root']
    lexpr = monkeys[root[0]]
    rexpr = monkeys[root[2]]
    a = lexpr.a - rexpr.a
    b = rexpr.b - lexpr.b
    return b/a

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
