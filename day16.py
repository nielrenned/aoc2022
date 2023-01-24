import networkx as nx
from queue import SimpleQueue

DAY = 16
RAW_INPUT = None
INPUT = None
SORTED_VALVES = None

def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/day{DAY:02}_test.txt'
    with open(path) as f:
        RAW_INPUT = f.read()

def parse_input():
    global INPUT
    G = nx.Graph()
    non_zero_valves = dict()
    for line in RAW_INPUT.split('\n')[:-1]:
        valve_name = line[6:8]
        flow_rate = int(line[line.find('=')+1:line.find(';')])
        if flow_rate != 0:
            non_zero_valves[valve_name] = flow_rate
        
        first_comma = line.find(',')
        connected_str = line[first_comma-2:]
        for connection in map(str.strip, connected_str.split(', ')):
            G.add_edge(valve_name, connection)
    
    shortest_paths = dict()
    for node, path_lengths in nx.all_pairs_shortest_path_length(G):
        shortest_paths[node] = path_lengths

    INPUT = (non_zero_valves, shortest_paths)


def should_prune(valves, time_remaining, pressure, most_pressure):
    """
    This function assumes that the valves are in the most optimal order 
    and location, i.e., highest-to-lowest pressures, and all 1 step away
    from the one before. If the pressure can't be improved in that situation,
    it can't be improved at all, so we can prune this branch.

    In testing, this reduced the number of checks from ~175000 to <~6000, so 
    over a 96% improvement.
    """
    nonzero_valve_pressures, _ = INPUT
    valves = sorted(valves, key=lambda x: -nonzero_valve_pressures[x])
    max_pressure = pressure
    for valve in valves:
        if time_remaining < 2:
            break
        time_remaining -= 2
        max_pressure += time_remaining * nonzero_valve_pressures[valve]
    return max_pressure < most_pressure

def solve_for_one_runner(potential_locations, time_alloted):
    nonzero_valve_pressures, shortest_paths = INPUT
    
    q = SimpleQueue()
    most_pressure_released = 0

    # (current location, valves to open, time remaining, pressure released)
    q.put(('AA', frozenset(potential_locations), time_alloted, 0))
    while not q.empty():
        loc, valves_remaining, time_remaining, pressure = q.get()
        for next_valve in valves_remaining:
            time_cost = shortest_paths[loc][next_valve] + 1
            if time_cost > time_remaining: continue

            new_time_remaining = time_remaining - time_cost
            new_pressure = pressure + (new_time_remaining * nonzero_valve_pressures[next_valve])
            new_valves = frozenset(valves_remaining - {next_valve})

            most_pressure_released = max(new_pressure, most_pressure_released)

            if len(new_valves) == 0 or new_time_remaining == 0:
                pass
            elif should_prune(new_valves, new_time_remaining, new_pressure, most_pressure_released):
                pass
            else:
                q.put((next_valve, new_valves, new_time_remaining, new_pressure))
    
    return most_pressure_released

def part1():
    nonzero_valve_pressures, _ = INPUT
    return solve_for_one_runner(nonzero_valve_pressures, 30)

def part2():
    nonzero_valve_pressures, _ = INPUT
    nonzero_valves = list(nonzero_valve_pressures.keys())

    max_pressure = 0

    pressures = dict()
    for n in range(0, 2**len(nonzero_valves)):
        valves = set()
        for i in range(len(nonzero_valves)):
            if (n & (1 << i)) > 0:
                valves.add(nonzero_valves[i])
        pressures[n] = solve_for_one_runner(valves, 26)
    
    for n in range(0, 2**len(nonzero_valves)):
        m = 2**len(nonzero_valves) - 1 - n
        max_pressure = max(pressures[n] + pressures[m], max_pressure)
    
    return max_pressure

def main():
    load_input()
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())

if __name__ == "__main__":
    main()
