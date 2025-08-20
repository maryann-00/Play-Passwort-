import numpy as np
import random
import re
import collections
import pygame
from mouseinfo import position

import Wort_in_scrabble_check
from Wort_in_scrabble_check import scrabble_check

pygame.init()

# Bildschirm einrichten
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
gruen = (0,204,0)
rot = (255, 0, 0)
gelb = (255, 255, 0)


rgb_farben = dict(weiss = (255, 255, 255), schwarz = (0, 0, 0), gruen = (0,204,0), rot = (255, 0, 0), gelb = (255, 255, 0), grau = (192, 192, 192))

breite= 500
hoehe = 700

bildschirm = pygame.display.set_mode((breite, hoehe))  # erstellt Spielfenster

runde = 0
# Matrix erstellen
"""
board = [["", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", ""]]
"""

bilder_pro_sekunde = 60 # Bilder pro Sekunde
spiel_uhr = pygame.time.Clock() # erstellt einen Zeitgeber, um die Bildrate zu steuern
schriftart = pygame.font.SysFont("freesensbold.ttf", 56)
wortlaenge = 5
anzahl_versuche = 6
hintergrundfarben = np.full((anzahl_versuche,wortlaenge),"weiss")

spielbrett = np.full((anzahl_versuche, wortlaenge), " ")

# Passwort aus Wortliste zufällig auswählen
wortliste = ["Apfel", "Birne", "Katze", "Blume", "Tisch",
    "Stuhl", "Lampe", "Besen", "Leine", "Faden",
    "Glanz", "Stein", "Fisch", "Blatt", "Krone",
    "Kerze", "Herde", "Kanne", "Farbe", "Segel",
    "Licht", "Handy", "Spule", "Puppe", "Radio",
    "Brett", "Ringe", "Kabel", "Stoff", "Welle",
    "Karte", "Nadel", "Lager", "Kugel", "Moped",
    "Boote", "Hafen", "Schaf", "Winde", "Rasen",
    "Hirte", "Zange", "Rolle", "Kamin", "Worte",
    "Weide", "Wagen", "Kiste", "Piano", "Laser"]
wortliste = [wort.upper() for wort in wortliste]
passwort = random.choice(wortliste).upper()
passwort_liste = list(passwort)
print(f"Das Passwort ist {passwort}")

#Initialbedingungen
buchstaben = 0
runde = 0
runde_aktiv = True # zu Beginn der Zeile haben wir weniger als 5 Buchstaben


def spielfeld_zeichnen():
    global runde
    global spielbrett
    #for i in range (0,wortlaenge):
        #pygame.Surface.fill(bildschirm, rgb_farben[hintergrundfarben[runde,i]], [i * 100 + 12, runde * 100 + 12, 75, 75])

    for spalte in range(0, 5):  # Endwert exkludiert
        for zeile in range(0, 6):
            pygame.Surface.fill(bildschirm, rgb_farben[hintergrundfarben[zeile, spalte]],
                                [spalte * 100 + 12, zeile * 100 + 12, 75, 75])

    for spalte in range(0, 5):  # Endwert exkludiert
        for zeile in range(0, 6):
            #pygame.Surface.fill(bildschirm, rgb_farben[hintergrundfarben[zeile, spalte]], [spalte * 100 + 12, runde * 100 + 12, 75, 75])
            pygame.draw.rect(bildschirm, schwarz, [spalte * 100 + 12, zeile * 100 + 12, 75, 75], 3,
                             5)  # 3 und 5 am Ende runden Vierecke ab
            buchstaben_text = schriftart.render(spielbrett[zeile][spalte], True, schwarz)
            bildschirm.blit(buchstaben_text, (spalte * 100+30, zeile * 100+25)) # Text erscheint auf Bildschirm
    pygame.draw.rect(bildschirm, rgb_farben["grau"], [buchstaben * 100 + 12, runde * 100 + 12, 75, 75], 3, 5)
    #pygame.draw.rect(bildschirm, gelb, [1 * 100 + 12, 0 * 100 + 12, 75, 75], 3,5)
    #pygame.draw.rect(bildschirm, rot, [2 * 100 + 12, 0 * 100 + 12, 75, 75], 3,5)


def buchstaben_einfaerben(eingabe, passwort, wortlaenge) -> list[str]:
    eingabe_liste = list(eingabe.upper())
    #print(eingabe_liste)
    passwort_liste = list(passwort.upper())
    #print(passwort_liste)
    farben = [None] * wortlaenge  # erstellt leere Liste in der Länge des Worts
    gelbe_buchstaben = []  # leere Liste erstellen
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
        for i in range(wortlaenge - 1, -1, -1):  # Schleife rückwärts
            if eingabe_liste[i] in gelb_mehrmals:
                if haeufigkeit_eingabe[eingabe_liste[i]] - anzahl_farbe_geaendert > haeufigkeit_passwort[
                    eingabe_liste[i]]:  # Buchstabe kommt häufiger im eingegebenen Wort vor als im Passwort
                    if farben[i] == 'gelb':  # es dürfen nur gelbe auf Rot gesetzt werden, keine grünen
                        farben[i] = 'rot'
                        anzahl_farbe_geaendert += 1

    print(farben)
    return farben


spiel_aktiv = True
while spiel_aktiv:  # Spielschleife starten
    spiel_uhr.tick(bilder_pro_sekunde)
    bildschirm.fill(weiss)
    spielfeld_zeichnen()

    for ereignis in pygame.event.get():  # erlaubt es, über alle von pygame erkannten Ereignisse zu iterieren
        if ereignis.type == pygame.QUIT:  # Anweisung, um das Spielfenster zu schließen
            spiel_aktiv = False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_BACKSPACE :
                spielbrett[runde][buchstaben] = ''
                # backspace löscht jeweils einen Buchstaben
            if ereignis.key == pygame.K_RETURN and buchstaben == 5: # Enter drücken, um in nächste Zeile zu gelangen
                eingabe = ("".join(spielbrett[runde][:wortlaenge]))
                print(eingabe)
                if scrabble_check(eingabe): # geprüftes Wort ist gültig
                    hintergrundfarben[runde,:] = buchstaben_einfaerben(eingabe, passwort, wortlaenge)
                    print(hintergrundfarben)
                    runde +=1
                buchstaben = 0
            if ereignis.key == pygame.K_LEFT and buchstaben > 0:
                buchstaben -= 1
            if ereignis.key == pygame.K_RIGHT and buchstaben < wortlaenge - 1:
                buchstaben += 1


        if ereignis.type == pygame.TEXTINPUT and runde_aktiv:
            eingabe_zeichen = ereignis.__getattribute__('text') # gibt ein Dictionary mit Attributen zurück
            print(ereignis)
            if re.match(r"[A-Z]",eingabe_zeichen.upper()):
                spielbrett[runde][buchstaben] = eingabe_zeichen.upper() # aktuelle Runde und aktuelles Zeichen
                buchstaben += 1

    if buchstaben == 5: # beendet den Versuch
        runde_aktiv = False
    if buchstaben < 5: # nur in diesem Fall dürfen Buchstaben hinzugefügt werden
        runde_aktiv = True

    pygame.display.flip()
pygame.quit()

