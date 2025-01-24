import sys
from math import gcd

# Funkcja rozszerzonego algorytmu Euklidesa do znajdowania współczynników x, y takich, że ax + by = NWD(a, b)
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)  # NWD, x, y
    else:
        g, y, x = extended_gcd(b % a, a)  # Rekurencyjne obliczenia
        return (g, x - (b // a) * y, y)   # Korekta współczynników

# Łączenie dwóch kongruencji w jedną za pomocą Chińskiego Twierdzenia o Resztach
def merge_congruences(a1, m1, a2, m2):
    # Obsługa przypadków, gdy jedna z kongruencji jest stałą (mod 0)
    if m1 == 0 and m2 == 0:
        return (a1, 0) if a1 == a2 else None  # Tylko jeśli stałe są równe
    elif m1 == 0:
        if (a1 - a2) % m2 == 0:
            return (a1, 0)  # Kongruencja stała spełniona
        else:
            return None
    elif m2 == 0:
        if (a2 - a1) % m1 == 0:
            return (a2, 0)  # Kongruencja stała spełniona
        else:
            return None
    else:
        # Obliczanie NWD i sprawdzanie spójności kongruencji
        g, x, y = extended_gcd(m1, m2)
        if (a2 - a1) % g != 0:
            return None  # Brak rozwiązania
        lcm = m1 // g * m2  # Najmniejsza wspólna wielokrotność
        x0 = (a1 + (x * (a2 - a1) // g) % (m2 // g) * m1) % lcm  # Rozwiązanie
        return (x0, lcm)

# Analiza ruchu pojedynczego dziecka: wykrywanie cykli i zbieranie ważnych kroków
def analyze_child(start_room, target_rooms, door_indices, transitions):
    visited = {}  # Śledzenie stanów (pokój, pozycja w cyklu)
    path = []     # Historia odwiedzonych pokoi
    current_room = start_room
    current_step = 0
    pattern_len = len(door_indices)
    pre_valid = []          # Kroki przed cyklem, gdy dziecko jest w celu
    cycle_start_idx = None  # Indeks początku cyklu
    cycle_length = None     # Długość cyklu
    cycle_offsets = []      # Przesunięcia w cyklu, gdy dziecko jest w celu

    while True:
        # Aktualny stan: (pokój, pozycja w cyklu ruchu)
        state = (current_room, current_step % pattern_len)
        if state in visited:
            # Wykryto cykl: zapisz indeks początku i długość
            cycle_start_idx = visited[state]
            cycle_length = len(path) - cycle_start_idx
            break
        visited[state] = len(path)  # Zapisz indeks stanu
        path.append(current_room)   # Dodaj pokój do ścieżki
        # Sprawdź, czy dziecko jest w pokoju docelowym (przed cyklem)
        if current_room in target_rooms:
            pre_valid.append(len(path) - 1)
        # Przejście do następnego pokoju zgodnie z wzorcem ruchu
        di = door_indices[current_step % pattern_len]  # Indeks drzwi
        current_room = transitions[current_room - 1][di]  # Nowy pokój
        current_step += 1

    # Zbierz przesunięcia w cyklu, gdy dziecko jest w pokoju docelowym
    for i in range(cycle_start_idx, len(path)):
        if path[i] in target_rooms:
            cycle_offsets.append(i - cycle_start_idx)

    return {
        'pre_valid': pre_valid,
        'cycle_start': cycle_start_idx,
        'cycle_length': cycle_length,
        'cycle_offsets': cycle_offsets
    }

# Główna funkcja rozwiązująca problem
def solve():
    # Wczytywanie danych z pliku
    with open("dane/13.in", "r") as file:
        n = int(file.readline().strip())  # Liczba pokoi
        k = int(file.readline().strip())  # Liczba dzieci
        start_rooms = list(map(int, file.readline().strip().split()))  # Początkowe pokoje
        target_rooms = set(map(int, file.readline().strip().split()))  # Pokoje docelowe
        move_pattern = file.readline().strip()  # Wzorzec ruchu (np. "ABAC")
        transitions = [list(map(int, file.readline().strip().split())) for _ in range(n)]  # Macierz przejść

    # Konwersja wzorca ruchu na indeksy drzwi (A=0, B=1, itd.)
    door_indices = [{'A':0, 'B':1, 'C':2, 'D':3}[c] for c in move_pattern]
    children_data = []  # Dane o ruchu każdego dziecka

    # Analiza ruchu każdego dziecka
    for start in start_rooms:
        data = analyze_child(start, target_rooms, door_indices, transitions)
        pre_valid = data['pre_valid']
        cycle_start = data['cycle_start']
        cycle_length = data['cycle_length']
        cycle_offsets = data['cycle_offsets']

        # Jeśli dziecko nigdy nie trafi do celu, zwróć "NIE"
        if not pre_valid and not cycle_offsets:
            print("NIE")
            return
        children_data.append((pre_valid, cycle_start, cycle_length, cycle_offsets))

    # Przetwarzanie kongruencji dla każdego dziecka
    current_congruences = [None]  # Bieżące kongruencje

    for idx, (pre_valid, cycle_start, cycle_length, cycle_offsets) in enumerate(children_data):
        possible = []
        # Dodaj kroki przed cyklem jako kongruencje stałe (mod 0)
        if pre_valid:
            for t in pre_valid:
                possible.append((t, 0))
        # Dodaj kroki w cyklu jako kongruencje modularne
        if cycle_offsets:
            for offset in cycle_offsets:
                a = (cycle_start + offset) % cycle_length
                possible.append((a, cycle_length))

        if not possible:
            print("NIE")
            return

        # Łączenie nowych kongruencji z istniejącymi
        new_congruences = []
        for cong in current_congruences:
            for pc in possible:
                if cong is None:
                    new_congruences.append(pc)
                else:
                    merged = merge_congruences(cong[0], cong[1], pc[0], pc[1])
                    if merged is not None:
                        new_congruences.append(merged)

        if not new_congruences:
            print("NIE")
            return

        # Usuwanie duplikatów kongruencji
        seen = set()
        unique_congruences = []
        for nc in new_congruences:
            key = (nc[0], nc[1]) if nc[1] != 0 else (nc[0], 0)
            if key not in seen:
                seen.add(key)
                unique_congruences.append(nc)
        current_congruences = unique_congruences

    # Sprawdzenie, czy istnieje rozwiązanie
    if not current_congruences:
        print("NIE")
        return

    # Znajdź minimalny krok spełniający wszystkie kongruencje
    min_step = None
    for cong in current_congruences:
        a, m = cong
        if m == 0:
            candidate = a  # Stała wartość
        else:
            candidate = a % m  # Najmniejsza nieujemna reszta
            while candidate < 0:
                candidate += m  # Poprawka dla ujemnych wartości
        # Sprawdź, czy kandydat pasuje do wszystkich dzieci
        valid = True
        for (pre_valid, cycle_start, cycle_length, cycle_offsets) in children_data:
            found = False
            if candidate in pre_valid:
                found = True  # Znaleziono w kroku przed cyklem
            else:
                if cycle_offsets:
                    t_in_cycle = candidate - cycle_start
                    if t_in_cycle >= 0 and (t_in_cycle % cycle_length) in cycle_offsets:
                        found = True  # Znaleziono w cyklu
            if not found:
                valid = False
                break
        if valid and (min_step is None or candidate < min_step):
            min_step = candidate

    # Wynik końcowy
    if min_step is not None:
        print(min_step)
    else:
        print("NIE")

if __name__ == "__main__":
    solve()