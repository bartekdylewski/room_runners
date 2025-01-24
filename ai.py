import time
import os
import hashlib

# Constants
PRINT_ALL = True  # print all additional info
INPUT_NAME = "test_01.in"  # input file name

ORDER_TO_ID = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3
}

def open_input(filename: str):
    # Open file with input data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "testy")
    file_path = os.path.join(input_dir, filename)
    
    with open(file_path, 'r') as file:
        return file.read()

def process_input(input_raw):
    '''
    Splits input into usable data needed for the problem.
    @return: Tuple containing rooms_total, kids_total, kids_start_rooms, end_rooms_set, order, rooms_doors
    '''
    input_lines = input_raw.strip().split('\n')
    rooms_total = int(input_lines[0])
    kids_total = int(input_lines[1])
    start_positions = list(map(int, input_lines[2].split()))
    end_rooms_set = set(map(int, input_lines[3].split()))
    order_raw = input_lines[4].strip()
    order = []
    for char in order_raw:
        order.append(ORDER_TO_ID[char])
    rooms_doors = []
    for i in range(5, len(input_lines)):
        doors = input_lines[i].split()
        for i in range(4):
            doors[i] = int(doors[i])
        rooms_doors.append(doors)
    return rooms_total, kids_total, start_positions, end_rooms_set, order, rooms_doors

def move_kids(actual_positions, rooms_doors, order, order_now, end_rooms_set):
    '''
    Moves kids to the next room based on the doors and current order.
    @return: List of new positions of kids.
    '''
    game_end = True
    for i in range(len(actual_positions)):
        actual_positions[i] = rooms_doors[actual_positions[i] - 1][order[order_now % len(order)]]
        # check if someone breaks end condition
        if actual_positions[i] not in end_rooms_set and game_end == True:
            game_end = False
            
    return actual_positions, game_end

def main(printAll):
    input_raw = open_input(INPUT_NAME)
    rooms_total, kids_total, start_positions, end_rooms_set, order, rooms_doors = process_input(input_raw)
    actual_positions = start_positions.copy()
    order_now = 0
    seen_positions = {}
    last_repeated = False

    time1 = time.time()
    i = 0
    while True:
        actual_positions, game_end = move_kids(actual_positions, rooms_doors, order, order_now, end_rooms_set)

        if game_end:
            if printAll:
                print(f"Last positions: {actual_positions}")
                print(f"Game ends at iteration {i}")

            delta_time = (time.time() - time1) * 1000
            skk = f"TAK, Time of execution in ms: {delta_time:.2f}ms"
            print("\x1b[42m{}\x1b[0m" .format(skk))
            break
        
        positions_tuple = tuple(actual_positions)
        if positions_tuple in seen_positions:
            if last_repeated:
                if printAll:
                    print(f"Position at {i} is same as {seen_positions[positions_tuple]}")
                    print(f"Positions at iteration {i:10d}: {str(positions_tuple)[:50]}...")
                    print(f"Positions at iteration {seen_positions[positions_tuple]:10d}: {str(positions_tuple)[:50]}...")
                    print("Game will not end.")

                delta_time = (time.time() - time1) * 1000
                skk = f"NIE, Time of execution in ms: {delta_time:.2f}ms"
                print("\x1b[32m{}\x1b[0m" .format(skk))
                break
            last_repeated = True
        else:
            last_repeated = False
        seen_positions[positions_tuple] = i
        
        order_now += 1
        i += 1
    
main(PRINT_ALL)