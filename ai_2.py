import os

# Constants
INPUT_NAME = "test_04.in"  # input file name

def open_input(filename: str):
    # Open file with input data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "testy")
    file_path = os.path.join(input_dir, filename)
    
    with open(file_path, 'r') as file:
        return file.read()

def process_input(input_raw):
    '''
    Przetwarza surowe dane wejściowe na struktury używane w algorytmie.
    Zwraca: (n, k, start_rooms, X, schema, doors)
    '''
    input_lines = input_raw.strip().split('\n')
    n = int(input_lines[0])
    k = int(input_lines[1])
    start_rooms = list(map(int, input_lines[2].split()))
    X = set(map(int, input_lines[3].split()))
    schema = input_lines[4].strip()
    
    # Przygotowanie mapy drzwi
    doors = []
    for i in range(5, len(input_lines)):
        a, b, c, d = map(int, input_lines[i].split())
        doors.append({'A': a, 'B': b, 'C': c, 'D': d})
    
    return n, k, start_rooms, X, schema, doors

# Główna logika programu
if __name__ == "__main__":
    input_raw = open_input(INPUT_NAME)
    n, k, start_rooms, X, schema, doors = process_input(input_raw)
    
    current_rooms = start_rooms.copy()
    S = len(schema)
    max_steps = n * S
    
    step = 0
    while True:
        # Sprawdź warunek końca gry
        if all(room in X for room in current_rooms):
            print(step-1)
            print("TAK")
            break
        
        if step == max_steps:
            print("MAX STEPS REACHED")
            print("NIE")
            break
        
        # Aktualizuj pozycje dzieci
        current_letter = schema[step % S]
        new_rooms = []
        for room in current_rooms:
            new_rooms.append(doors[room - 1][current_letter])
        current_rooms = new_rooms
        step += 1
    
    