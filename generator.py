import random
import os

# 1 <= n <= 1000 pokojow
# 1 <= k <= 100 dzieci
# 1 <= #X <= 20 docelowe pokoje
# schemat portali/drzwi ABCD (Y razy)
# n wierszy z schematem portali ABCD

n = 1000
k = 100
X = 20
Y = 10

def list_to_proper_string(list:list):
    string = str(list)[1:-1]
    for char in string:
        if char == ",":
            string = string.replace(char, "")
    return string

rooms_count = random.randint(100,n)
kids = random.randint(50,k)

# Generowanie pozycji startowych dzieci
start_positions = [random.randint(1, n // 2) for _ in range(k)]
start_positions_str = list_to_proper_string(start_positions)


# Generowanie pokojów końcowych (rozmieszczonych równomiernie)
end_positions = sorted(random.sample(range(n // 2, n + 1), X))
end_positions_str = list_to_proper_string(end_positions)

# Generowanie schematu portali
order = "".join(random.choices(['A', 'B', 'C', 'D'], k=random.randint(1, Y)))

# Generowanie drzwi dla każdego pokoju
rooms = []
for i in range(1, n + 1):
    room = []
    for _ in range(4):
        # Drzwi prowadzą do pokojów w promieniu +/- 10 od bieżącego pokoju
        door_to = (i + random.randint(-100, 100)) % n + 1
        room.append(door_to)
    rooms.append(list_to_proper_string(room))

# Tworzenie linii do pliku
lines = [
    f"{rooms_count}\n",  # liczba pokojów
    f"{kids}\n",  # liczba dzieci
    f"{start_positions_str}\n",  # lista dzieci w pokojach startowych
    f"{end_positions_str}\n",  # pokoje końcowe
    f"{order}\n",  # schemat portali
]
lines.extend(f"{room}\n" for room in rooms)

# budowanie ścieżki do folderu input
current_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(current_dir, "input")
os.makedirs(input_dir, exist_ok=True)

# budowanie ścieżki do pliku
file_path = os.path.join(input_dir, "generated.txt")

# zapisanie pliku
with open(file_path, "w") as file:
    file.writelines(lines)

print(f"Generated file successfully at {file_path}.")