import numpy as np
import random

#Passwort aus Wortliste zufällig auswählen
wortliste = ['Apfel', 'Birne', 'Katze', 'Blume', 'Tisch', 'Stuhl', 'Lampe', 'Besen', 'Leine']
passwort = random.choice(wortliste).upper()
passwortListe = list(passwort)
print(f"Das Passwort ist {passwort}")

#Wort eingeben
eingabe = input("Gib ein Wort ein: ").upper()
eingabeListe = list(eingabe)
print("Du hast das Wort eingegeben:", eingabe)

#Prüfen, ob eingebenes Wort in der Wortliste enthalten ist
if (eingabe in wortliste): 
    print("Das Wort ist in der Liste!")
else: 
    (print("Das Wort ist nicht in der Liste!"))

#Buchstaben check
for i in range (0,len(passwortListe)):
    print(f"{i}, Buchstabe Eingabe {eingabeListe[i]}, Buchstabe Passwort {passwortListe[i]}")
    if eingabeListe[i] == passwortListe[i]:
        print(f"Buchstabe {i + 1} ist grün")
    elif (eingabeListe[i] not in passwortListe):
        print(f"Buchstabe {i + 1} ist rot")
    else:
        print(f"Buchstabe {i + 1} ist gelb")


#Prüfen ob eingebenes Wort gleich dem Passwort ist
if (eingabe == passwort):
    print("Du hast das Passwort erraten :)")
