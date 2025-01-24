import sys
from itertools import product

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def solve_crt(congruences):
    x = 0
    mod = 1
    for (a, c) in congruences:
        g, p, q = extended_gcd(mod, c)
        if (a - x) % g != 0:
            return None
        lcm = mod // g * c
        tmp = ((a - x) // g * p) % (c // g)
        x += mod * tmp
        mod = lcm
        x %= mod
    return (x, mod)

def main():
    if len(sys.argv) < 2:
        print("Please provide the input file name as an argument.")
        return

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        k = int(f.readline().strip())
        starting_rooms = list(map(int, f.readline().strip().split()))
        X = set(map(int, f.readline().strip().split()))
        pattern = f.readline().strip()
        doors = []
        for _ in range(n):
            doors.append(list(map(int, f.readline().strip().split())))
    
    children = []
    possible = True
    
    for room in starting_rooms:
        current_room = room
        visited = dict()
        steps = []
        in_x_times = []
        current_pattern_idx = 0
        cycle_start = -1
        cycle_length = 0
        
        for step in range(2 * 10**6):
            state = (current_room, current_pattern_idx)
            if state in visited:
                cycle_start = visited[state]
                cycle_length = step - cycle_start
                break
            visited[state] = step
            if current_room in X:
                in_x_times.append(step)
            direction = pattern[current_pattern_idx]
            door_idx = ord(direction) - ord('A')
            current_room = doors[current_room - 1][door_idx]
            current_pattern_idx = (current_pattern_idx + 1) % len(pattern)
        
        prefix_times = [t for t in in_x_times if t < cycle_start]
        cycle_steps = [t for t in in_x_times if t >= cycle_start]
        
        cycle_constraints = set()
        for t in cycle_steps:
            a = (t - cycle_start) % cycle_length
            real_a = (cycle_start + a) % cycle_length
            cycle_constraints.add((real_a, cycle_length, cycle_start))
        
        cycle_constraints = list(cycle_constraints)
        children.append({
            'prefix': prefix_times,
            'cycle': cycle_constraints,
        })
        if not prefix_times and not cycle_constraints:
            possible = False
    
    if not possible:
        print("NIE")
        return
    
    prefix_candidates = set()
    for child in children:
        prefix_candidates.update(child['prefix'])
    prefix_candidates = sorted(prefix_candidates)
    
    min_t = None
    for t0 in prefix_candidates:
        valid = True
        for child in children:
            if t0 in child['prefix']:
                continue
            found = False
            for (a, c, s) in child['cycle']:
                if t0 >= s and (t0 - a) % c == 0:
                    found = True
                    break
            if not found:
                valid = False
                break
        if valid:
            if min_t is None or t0 < min_t:
                min_t = t0
    
    cycle_options = [child['cycle'] for child in children]
    has_empty = any(len(opt) == 0 for opt in cycle_options)
    if not has_empty:
        for combination in product(*cycle_options):
            congruences = []
            s_list = []
            for (a, c, s) in combination:
                congruences.append((a, c))
                s_list.append(s)
            max_s = max(s_list)
            res = solve_crt(congruences)
            if res is None:
                continue
            x, mod = res
            if mod == 0:
                continue
            if x >= max_s:
                candidate = x
            else:
                k = (max_s - x + mod - 1) // mod
                candidate = x + k * mod
            if min_t is None or candidate < min_t:
                min_t = candidate
    
    if min_t is not None:
        print(min_t)
    else:
        print("NIE")

if __name__ == "__main__":
    main()