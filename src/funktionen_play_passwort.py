import collections
import os
from typing import List


def buchstaben_einfaerben(eingabe: str, passwort: str) -> list[None]:
    """
    Gibt eine Farbe pro Buchstaben zurück
    gruen: Buchstabe ist an der richtigen Position
    gelb: Buchstabe kommt im Wort vor, aber an einer anderen Position
    rot: Buchstabe kommt nicht im Wort vor
    :param eingabe: Wort, das überprüft werden soll
    :param passwort: Wort, das erraten werden soll
    :return: Liste von Farben (rot,gelb oder gruen) als Strings, die Länge der Liste entspricht der Anzahl der Buchstaben
    """
    if len(eingabe) != len(passwort):
        raise ValueError("Das eingegebene Wort muss genauso lang sein wie das Passwort")
    wortlaenge = len(passwort)
    eingabe_liste = list(eingabe.upper())
    # print(eingabe_liste)
    passwort_liste = list(passwort.upper())
    # print(passwort_liste)
    farben = [None] * wortlaenge  # erstellt leere Liste in der Länge des Worts
    gelbe_buchstaben = []  # leere Liste erstellen
    for i in range(0, wortlaenge):
        # print(f"{i}, Buchstabe Eingabe {eingabe_liste[i]}, Buchstabe Passwort {passwort_liste[i]}")
        if eingabe_liste[i] == passwort_liste[i]:
            farben[i] = "gruen"
            # print(f"Buchstabe {i + 1} ist grün")
        elif eingabe_liste[i] not in passwort_liste:
            farben[i] = "rot"
            # print(f"Buchstabe {i + 1} ist rot")
        else:
            farben[i] = "gelb"
            # print(f"Buchstabe {i + 1} ist gelb")
            gelbe_buchstaben.append(eingabe_liste[i])

    # print(farben)

    # Prüfen, ob ein Buchstabe gelb ist und mehrmals im eingegebenen Wort vorkommt
    haeufigkeit_eingabe = collections.Counter(eingabe_liste)  # zählt wie häufig ein Buchstabe im Wort vorkommt
    haeufigkeit_passwort = collections.Counter(passwort_liste)
    buchstabe_eingabe_mehrmals = [buchstabe for (buchstabe, anzahl) in haeufigkeit_eingabe.items() if anzahl > 1]
    gelb_mehrmals = set(gelbe_buchstaben) & set(buchstabe_eingabe_mehrmals)

    # falsch gelbe auf Rot setzen
    anzahl_farbe_geaendert = 0
    if len(gelb_mehrmals) > 0:  # wenn die Länge eines Sets größer als 0 ist, ist das Set nicht leer
        for i in range(wortlaenge - 1, -1, -1):  # Schleife rückwärts durch eingegebenes Wort
            if eingabe_liste[i] in gelb_mehrmals:
                if haeufigkeit_eingabe[eingabe_liste[i]] - anzahl_farbe_geaendert > haeufigkeit_passwort[
                    eingabe_liste[i]]:  # Buchstabe kommt häufiger im eingegebenen Wort vor als im Passwort
                    if farben[i] == 'gelb':  # es dürfen nur gelbe auf Rot gesetzt werden, keine grünen
                        farben[i] = 'rot'
                        anzahl_farbe_geaendert += 1

    # print(farben)
    return farben


def ist_wort_erlaubt(wort: str) -> bool:
    """Prüft, ob ein Wort (bei Scrabble) erlaubt ist"""
    wort = wort.upper()
    dateipfad = os.path.join(os.path.dirname(__file__), '..', 'data', 'wortliste_fuenf_buchstaben.txt')
    with open(dateipfad, "r", encoding="utf8") as datei:
        erlaubte_woerter = set(datei.read().split())
        return wort in erlaubte_woerter
