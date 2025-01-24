n = int(input())
k = int(input())
start_rooms = list(map(int, input().split()))
X = set(map(int, input().split()))
schema = input().strip()

# Przygotowanie mapy drzwi dla każdego pokoju
doors = []
for _ in range(n):
    a, b, c, d = map(int, input().split())
    doors.append({'A': a, 'B': b, 'C': c, 'D': d})

current_rooms = start_rooms.copy()
S = len(schema)
max_steps = n * S

for step in range(max_steps + 1):
    # Sprawdź, czy wszystkie dzieci są w X
    if all(room in X for room in current_rooms):
        print(step)
        exit()
    
    if step == max_steps:
        break  # Nie sprawdzaj już dalej
    
    # Aktualna litera schematu
    current_letter = schema[step % S]
    
    # Przesuń każde dziecko zgodnie z literą
    new_rooms = []
    for room in current_rooms:
        next_room = doors[room - 1][current_letter]
        new_rooms.append(next_room)
    current_rooms = new_rooms

print("NIE")