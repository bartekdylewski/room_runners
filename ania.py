import time

# Zmienna przechowująca dane wejściowe
input_data = []

winning_rooms = []  # zbiór kluczowy do wygranej - X
lista_polozen = []  # gdzie jest dziecko w danym kroku, lista ta zawiera słowniki licząc dzieci
siatka = []         # siatka polega na liście 2 wymiarowej :)

# Odczyt danych z pliku
with open('input_0', 'r') as data_in:
    for i in data_in:
        line = []
        for element in i.split():
            line.append(int(element) if element.isdigit() else element)  # Konwersja elementów na liczby całkowite oprocz drzwi ABCD
        input_data.append(line)
print(input_data)

rooms = int(input_data[0][0])   # liczba pokoi
kids = int(input_data[1][0])    # liczba dzieci
input_pattern = str(input_data[4][0]) # Cały ciąg wprowadzonego patternu czyli np CAD
pattern = [] # tu przechowywane są odzielne kroki potem zamieniane na przypisane krokom wartości

for i in range(len(input_pattern)):
    pattern.append(input_pattern[i])        # kroki drzwi np CAD zamieniane na 'C' 'A' 'D'
    if pattern[i] == 'A':           # od tego momentu zamieniamy na wartości liczbowe
        pattern[i] = 0
    elif pattern[i] == 'B':
        pattern[i] = 1
    elif pattern[i] == 'C':
        pattern[i] = 2
    elif pattern[i] == 'D':
        pattern[i] = 3
print(pattern)

for i in input_data[3]:  # wrzucamy do listy kluczowe pokoje zapewniające wygraną
    winning_rooms.append(int(i))

for i in range(kids):  # pętla elegancko przypisuje każdemu dziecku numer pokoju startowego
    lista_polozen.append({i: int(input_data[2][i])})

print(lista_polozen)

# tworzenie siatki
for i in range(5, 5 + rooms):  # od piątego wiersza zaczyna się definicja siatki
    siatka.append(input_data[i])
print(siatka)

# Używamy patternu ABCD, pokoi id w zwiazku z połozeniem dzieci na siatce
step = 1
pattern_choice = 0 #sledzi i pilnuje aby pattern był pokolei C -> A -> D (i od poczatku)
timeout = time.time() + 5  # 5 sekund od tego momentu w programie
while True:
    output = 0  # pokazuje czy gra się skończy sukcesem
    zmiany = []  # lista przechowująca zmienione miejsca

    for kid_movement in range(kids):
        x = lista_polozen[kid_movement] #x to zmienna pomocnicza ktora przechowuje słownik aktualnego dziecka
        current_room = x[kid_movement]  #numer pokoju w ktorym aktualnie jest
        next_room = siatka[current_room - 1][pattern[pattern_choice]]  # -1 bo indexy zaczynają się od 0, a pokój jest oznaczany od 1
        x[kid_movement] = next_room

        # Sprawdzenie, czy dziecko dotarło do pokoju wygrywającego
        if next_room in winning_rooms:
            output += 1

    if output == kids or time.time() > timeout:
        break

    pattern_choice += 1
    if pattern_choice >= len(pattern):
        pattern_choice = 0
    step += 1

if output == kids:
    print("\nGra została wygrana po",step, "krokach.")
else:
    print("\nNIE")