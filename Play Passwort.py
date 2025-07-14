import random
import collections
import pygame

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height)) #create game window

run = True
while run: #initialize game loop

    for event in pygame.event.get(): #allows us to iterate over all the events that pygame picks up
        if event.type == pygame.QUIT: #statement to close pygame window
            run = False

pygame.quit()

###


laenge = 5

# Passwort aus Wortliste zufällig auswählen
wortliste = ['Apfel', 'Birne', 'Katze', 'Blume', 'Tisch', 'Stuhl', 'Lampe', 'Besen', 'Leine']
wortliste = [wort.upper() for wort in wortliste]
passwort = random.choice(wortliste).upper()
passwort_liste = list(passwort)
print(f"Das Passwort ist {passwort}")


# Worteingabe

def wort_eingabe():
    eingabe = input("Gib ein Wort ein: ").upper()
    eingabe_liste = list(eingabe)

    print("Du hast das Wort eingegeben:", eingabe)
    return eingabe, eingabe_liste

def richtige_wortlaenge(eingabe):
    if (len(eingabe) != 5):
        print("Das Wort muss 5 Buchstaben haben")
    return len(eingabe) == 5


def wort_in_wortliste(eingabe, wortliste):
    if eingabe in wortliste:
        print("Das Wort ist in der Liste!")  # später löschen, irreführend für den Spieler
        return True
    else:
        print("Dein Wort existiert nicht. Bitte wähle ein anderes Wort!")
        return False

passwort_erraten = False
while not passwort_erraten:
    eingabe, eingabe_liste = wort_eingabe()
    if not richtige_wortlaenge(eingabe):
        continue

    if not wort_in_wortliste(eingabe, wortliste):
        continue

    # Buchstaben check
    farben = [None] * laenge  # erstellt leere Liste in der Länge des Worts
    gelbe_buchstaben = []  # leere liste erstellen
    for i in range(0, len(passwort_liste)):
        print(f"{i}, Buchstabe Eingabe {eingabe_liste[i]}, Buchstabe Passwort {passwort_liste[i]}")
        if eingabe_liste[i] == passwort_liste[i]:
            farben[i] = "gruen"
            print(f"Buchstabe {i + 1} ist grün")
        elif (eingabe_liste[i] not in passwort_liste):
            farben[i] = "rot"
            print(f"Buchstabe {i + 1} ist rot")
        else:
            farben[i] = "gelb"
            print(f"Buchstabe {i + 1} ist gelb")
            gelbe_buchstaben.append(eingabe_liste[i])

    print(farben)

    # Prüfen, ob ein Buchstabe gelb ist und mehrmals im eingegebenen Wort vorkommt
    haeufigkeit_eingabe = collections.Counter(eingabe_liste)  # zählt wie häufig ein Buchstabe im Wort vorkommt
    haeufigkeit_passwort = collections.Counter(passwort_liste)
    buchstabe_eingabe_mehrmals = [buchstabe for (buchstabe, anzahl) in haeufigkeit_eingabe.items() if anzahl > 1]
    gelb_mehrmals = set(gelbe_buchstaben) & set(buchstabe_eingabe_mehrmals)

    # falsch gelbe auf Rot setzen
    anzahl_farbe_geaendert = 0
    if (len(gelb_mehrmals) > 0):  # wenn die Länge eines Sets größer als 0 ist, ist das Set nicht leer
        for i in range(laenge - 1, -1, -1):  # schleife rückwärts
            if eingabe_liste[i] in gelb_mehrmals:
                if haeufigkeit_eingabe[eingabe_liste[i]] - anzahl_farbe_geaendert > haeufigkeit_passwort[
                    eingabe_liste[i]]:  # Buchstabe kommt häufiger im eingebenen Wort vor als im Passwort
                    if farben[i] == 'gelb':  # es dürfen nur gelbe auf Rot gesetzt werden keine grünen
                        farben[i] = 'rot'
                        anzahl_farbe_geaendert += 1

    print(farben)

    # Prüfen, ob eingebenes Wort gleich dem Passwort ist
    if (eingabe == passwort):
        passwort_erraten = True
        print("Du hast das Passwort erraten :)")