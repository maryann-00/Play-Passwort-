import numpy as np
import random

import collections

laenge = 5

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
farben = [None]* laenge # erstellt leere Liste in der Länge des Worts
gelbeBuchstaben = [] #leere liste erstellen
for i in range (0,len(passwortListe)):
    print(f"{i}, Buchstabe Eingabe {eingabeListe[i]}, Buchstabe Passwort {passwortListe[i]}")
    if eingabeListe[i] == passwortListe[i]:
        farben[i] = "gruen"
        print(f"Buchstabe {i + 1} ist grün")
    elif (eingabeListe[i] not in passwortListe):
        farben[i] = "rot"
        print(f"Buchstabe {i + 1} ist rot")
    else:
        farben[i] = "gelb"
        print(f"Buchstabe {i + 1} ist gelb")
        gelbeBuchstaben.append(eingabeListe[i])

print (farben)

#Prüfen ob ein Buchstabe gelb ist und mehrmals im eingegebenen Wort vorkommt
haeufigkeitEingabe = collections.Counter(eingabeListe) #zählt wie häufig ein Buchstabe im Wort vorkommt
haeufigkeitPasswort = collections.Counter(passwortListe)
buchstabeEingabeMehrmals = [buchstabe for (buchstabe, anzahl) in haeufigkeitEingabe.items() if anzahl > 1]
gelbMehrmals = set(gelbeBuchstaben) & set(buchstabeEingabeMehrmals)

#falsch gelbe auf rot setzen
anzahlFarbeGeaendert = 0
if (len(gelbMehrmals) > 0): #wenn die Länge eines Sets größer als 0 ist, ist das Set nicht leer
    for i in range(laenge - 1, -1, -1): #schleife rückwärts
        if eingabeListe[i] in gelbMehrmals:
            if haeufigkeitEingabe[eingabeListe[i]] - anzahlFarbeGeaendert > haeufigkeitPasswort[eingabeListe[i]]: #Buchstabe kommt häufiger im eingebenen Wort vor als im Passwort
                if farben[i] == 'gelb': #es dürfen nur gelbe auf rot gesetzt werden keine grünen
                    farben[i] = 'rot'
                    anzahlFarbeGeaendert += 1


print(farben)




#Prüfen, ob eingebenes Wort gleich dem Passwort ist
if (eingabe == passwort):
    print("Du hast das Passwort erraten :)")
