from collections import namedtuple

DAY = 7
RAW_INPUT = None
INPUT = None

def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/day{DAY:02}_test.txt'
    with open(path) as f:
        RAW_INPUT = f.read()


class Directory:
    def __init__(self, name: str = None, parent = None):
        self.name = name
        self.parent = parent
        self.children = []
    
    def calculate_size(self):
        size = 0
        for child in self.children:
            if type(child) == File:
                size += child.size
            else:
                size += child.calculate_size()
        return size


class File:
    def __init__(self, name: str = None, size: int = 0):
        self.name = name
        self.size = size


def parse_input():
    global INPUT
    INPUT = []
    LINES = RAW_INPUT.split('\n')[:-1]
    
    base_directory = Directory('/', None)
    
    i = 0
    while i < len(LINES):
        # We assume we're always starting with a command
        command = LINES[i][2:]
        output = ''
        
        # Capture command output
        while i+1 < len(LINES) and (not LINES[i+1].startswith('$')):
            output += LINES[i+1] + '\n'
            i += 1
        
        # Build file structure
        if command.startswith('cd'):
            _, dir = command.split()
            if dir == '/':
                current_directory = base_directory
            elif dir == '..':
                current_directory = current_directory.parent
            else:
                for child in current_directory.children:
                    if type(child) == Directory and child.name == dir:
                        current_directory = child
                        break
                else:
                    print(f'Directory {dir} is not a child of {current_directory.name}.')
                    exit(-1)
        elif command.startswith('ls'):
            for line in output.split('\n')[:-1]:
                info, name = line.split(' ')
                if info == 'dir':
                    new_directory = Directory(name, current_directory)
                    current_directory.children.append(new_directory)
                elif info.isnumeric():
                    new_file = File(name, int(info))
                    current_directory.children.append(new_file)
        
        i += 1
    
    INPUT = base_directory


def print_directory(dir: Directory, indent=0):
    indent_str = ' '*indent
    print(f'{indent_str}- {dir.name} (dir, size={dir.calculate_size()})')
    for child in sorted(dir.children, key=lambda c: c.name):
        if type(child) == Directory:
            print_directory(child, indent=indent+2)
        else:
            indent_str = ' '*(indent+2)
            print(f'{indent_str}- {child.name} (file, size={child.size})')


def get_all_directories(base_dir: Directory):
    directories = [base_dir]
    for child in base_dir.children:
        if type(child) == Directory:
            directories += get_all_directories(child)
    return directories


def part1():
    total_size = 0
    for dir in get_all_directories(INPUT):
        dir_size = dir.calculate_size()
        if dir_size <= 100000:
            total_size += dir_size
    
    return total_size


def part2():
    TOTAL_DISK_SPACE = 70000000
    current_unused = TOTAL_DISK_SPACE - INPUT.calculate_size()
    NEED_TO_FREE = 30000000 - current_unused
    
    candidates = [dir for dir in get_all_directories(INPUT) if dir.calculate_size() >= NEED_TO_FREE]
    candidates.sort(key=lambda d: d.calculate_size())
    return candidates[0].calculate_size()


def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()
