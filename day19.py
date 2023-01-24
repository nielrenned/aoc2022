import re
from collections import namedtuple, defaultdict
from queue import SimpleQueue, PriorityQueue
from enum import IntEnum
import math

DAY = 19
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
    line_fmt = r'Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
    blueprint_parser = re.compile(line_fmt)    
    INPUT = []
    for line in RAW_INPUT.split('\n')[:-1]:
        nums = list(map(int, blueprint_parser.fullmatch(line).groups()))
        ore_robot_cost = (nums[0], 0, 0, 0)
        clay_robot_cost = (nums[1], 0, 0, 0)
        obsidian_robot_cost = (nums[2], nums[3], 0, 0)
        geode_robot_cost = (nums[4], 0, nums[5], 0)
        INPUT.append(Blueprint(ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost))

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

Blueprint = namedtuple('Blueprint', ['ore_robot_cost', 'clay_robot_cost', 'obsidian_robot_cost', 'geode_robot_cost'])

class Factory:
    def __init__(self, blueprint: Blueprint, starting_robots: tuple, starting_materials: tuple = (0,0,0,0)):
        self.blueprint = blueprint
        self.robots = list(starting_robots)
        self.materials = list(starting_materials)
        self.prev_materials = self.materials[:]
        
        self.max_materials_needed = [0, 0, 0, 0]
        for material in range(4):
            for cost in self.blueprint:
                current = self.max_materials_needed[material]
                self.max_materials_needed[material] = max(current, cost[material])
    
    def mine_resources(self, n=1):
        self.prev_materials = self.materials[:]
        for i in range(4):
            self.materials[i] += n*self.robots[i]
    
    def build_robot(self, robot_type: int):
        for i in range(4):
            self.materials[i] -= self.blueprint[robot_type][i]
        self.robots[robot_type] += 1
    
    def time_needed_to_build_robot(self, robot_type: int):
        max_time_needed = 0
        for i, cost in enumerate(self.blueprint[robot_type]):
            if cost == 0: continue
            if cost > 0 and self.robots[i] == 0: return 2**32
            
            robots_of_type = self.robots[i]
            time_needed = int(math.ceil((cost - self.materials[i]) / robots_of_type))
            max_time_needed = max(max_time_needed, time_needed)
        return max_time_needed + 1
    
    def should_build_robot(self, material: int):
        # We should always build a GEODE robot if we can. For the rest
        # of the types, it's wasteful to build more robots than the
        # highest amount of materials we'd need in one minute.
        return (material == GEODE or self.robots[material] < self.max_materials_needed[material])

def copy_factory(factory: Factory):
    new_factory = Factory(factory.blueprint, factory.robots[:], factory.materials[:])
    return new_factory

def calculate_max_geode_yield(
        blueprint: Blueprint,
        total_time: int = 24,
        starting_robots: tuple = (1,0,0,0)):
    
    initial_factory = Factory(blueprint, starting_robots)
    q = SimpleQueue()
    q.put((0, initial_factory))
    seen_states = set([(0, initial_factory)])
    
    max_geodes = 0

    while not q.empty():
        time_elapsed, factory = q.get()
        
        time_left = total_time - time_elapsed
        total_geodes_producable = time_left*factory.robots[GEODE] + factory.materials[GEODE]
                
        max_geodes = max(max_geodes, total_geodes_producable)
        
        # If it's the last minute, this branch ends here.
        # We could build a robot, but it can't mine anything.
        if time_elapsed >= total_time:
            continue
        
        # If we optimistically assume that we build a geode robot every minute
        # and that's still not enough to reach the best we've seen, prune.
        max_possible_geodes = (time_left - 1)*time_left // 2
        max_possible_geodes += time_left*factory.robots[GEODE]
        max_possible_geodes += factory.materials[GEODE]
        if max_geodes >= max_possible_geodes:
            continue

        # Otherwise, we'll time-jump to building each robot.
        # Re-qeueing without building a robot is a waste.
        for material in range(4):
            if not factory.should_build_robot(material): continue
            
            time_needed = factory.time_needed_to_build_robot(material)
            if time_needed < time_left: # building a robot during the last minute is silly.
                factory_copy = copy_factory(factory)
                factory_copy.mine_resources(time_needed)
                factory_copy.build_robot(material)
                q.put((time_elapsed + time_needed, factory_copy))

    return max_geodes

def part1():
    total_quality = 0
    for i, blueprint in enumerate(INPUT):
        max_yield = calculate_max_geode_yield(blueprint)
        total_quality += (i+1)*max_yield
    return total_quality

def part2():
    total_quality = 1
    for blueprint in INPUT[:3]:
        max_yield = calculate_max_geode_yield(blueprint, 32)
        total_quality *= max_yield
    return total_quality
        

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
