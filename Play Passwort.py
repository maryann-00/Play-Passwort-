import numpy as np
import random

import collections

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


def wort_in_wortliste(eingabe, wortliste):
    if eingabe in wortliste:
        print("Das Wort ist in der Liste!")  # später löschen, irreführend für den Spieler
        return True
    else:
        print("Dein Wort existiert nicht. Bitte wähle ein anderes Wort!")
        return False


eingabe, eingabe_liste = wort_eingabe()
while not wort_in_wortliste(eingabe, wortliste):
    eingabe, eingabe_liste = wort_eingabe()


# Prüfen, ob eingebenes Wort in der Wortliste enthalten ist
if (eingabe in wortliste):
    print("Das Wort ist in der Liste!")
else:
    (print("Bitte wähle ein anderes Wort!"))

# Buchstaben check
farben = [None] * laenge  # erstellt leere Liste in der Länge des Worts
gelbeBuchstaben = []  # leere liste erstellen
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
        gelbeBuchstaben.append(eingabe_liste[i])

print(farben)

# Prüfen ob ein Buchstabe gelb ist und mehrmals im eingegebenen Wort vorkommt
haeufigkeitEingabe = collections.Counter(eingabe_liste)  # zählt wie häufig ein Buchstabe im Wort vorkommt
haeufigkeitPasswort = collections.Counter(passwort_liste)
buchstabeEingabeMehrmals = [buchstabe for (buchstabe, anzahl) in haeufigkeitEingabe.items() if anzahl > 1]
gelbMehrmals = set(gelbeBuchstaben) & set(buchstabeEingabeMehrmals)

# falsch gelbe auf rot setzen
anzahlFarbeGeaendert = 0
if (len(gelbMehrmals) > 0):  # wenn die Länge eines Sets größer als 0 ist, ist das Set nicht leer
    for i in range(laenge - 1, -1, -1):  # schleife rückwärts
        if eingabe_liste[i] in gelbMehrmals:
            if haeufigkeitEingabe[eingabe_liste[i]] - anzahlFarbeGeaendert > haeufigkeitPasswort[
                eingabe_liste[i]]:  # Buchstabe kommt häufiger im eingebenen Wort vor als im Passwort
                if farben[i] == 'gelb':  # es dürfen nur gelbe auf rot gesetzt werden keine grünen
                    farben[i] = 'rot'
                    anzahlFarbeGeaendert += 1

print(farben)

# Prüfen, ob eingebenes Wort gleich dem Passwort ist
if (eingabe == passwort):
    print("Du hast das Passwort erraten :)")