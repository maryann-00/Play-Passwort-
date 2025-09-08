from collections import Counter
import numpy as np
import random
import re
import collections
import sys
import time
import pygame
from mouseinfo import position
import Wort_in_scrabble_check
from Wort_in_scrabble_check import scrabble_check


def spielende_anzeigen(nachricht1, nachricht2=None):
    schrift = pygame.font.SysFont("freesensbold.ttf", 24)
    text1 = schrift.render(nachricht1, True, (0,0,0))
    rect1 = text1.get_rect(center=(breite // 2, hoehe // 2 - 20))

    # Bildschirm leeren
    bildschirm.fill(rgb_farben["weiss"])
    bildschirm.blit(text1, rect1)

    # Optional: Zweite Zeile
    if nachricht2:
        text2 = schrift.render(nachricht2, True, (0,0,0))
        rect2 = text2.get_rect(center=(breite // 2, hoehe // 2 + 20))
        bildschirm.blit(text2, rect2)
    pygame.display.flip()

    bildschirm_angezeigt = True
    while bildschirm_angezeigt:
        for ereignis in pygame.event.get():  # erlaubt es, über alle von pygame erkannten Ereignisse zu iterieren
            if ereignis.type == pygame.QUIT:  # Anweisung, um das Spielfenster zu schließen
                sys.exit()

def meldung_anzeigen(nachricht, dauer=1500):
    """Zeigt eine kurze Meldung am unteren Bildschirmrand an (ms)."""
    schrift = pygame.font.SysFont("freesensbold.ttf", 32)
    text = schrift.render(nachricht, True, (255, 0, 0))
    rect = text.get_rect(center=(breite // 2, hoehe - 50))
    bildschirm.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(4000)  # blockiert kurz das Spiel

#Initialbedingungen
wortlaenge = 5
anzahl_versuche = 6
anzahl_buchstaben = 0
runde = 0
position_zeile = 0
hintergrundfarben = np.full((anzahl_versuche,wortlaenge),"weiss")
rgb_farben = dict(weiss = (255, 255, 255), schwarz = (0, 0, 0), gruen = (0,204,0), rot = (255, 0, 0), gelb = (255, 255, 0), grau = (192, 192, 192))

#Bildschirm
breite= 500
hoehe = 700
pygame.init()
bildschirm = pygame.display.set_mode((breite, hoehe))  # erstellt Spielfenster
schriftart = pygame.font.SysFont("freesensbold.ttf", 56)
spielbrett = np.full((anzahl_versuche, wortlaenge), " ")
bilder_pro_sekunde = 60 # Bilder pro Sekunde
spiel_uhr = pygame.time.Clock() # erstellt einen Zeitgeber, um die Bildrate zu steuern

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

def spielfeld_zeichnen():
    global runde
    global spielbrett

    for spalte in range(0, 5):  # Endwert exkludiert
        for zeile in range(0, 6):
            pygame.Surface.fill(bildschirm, rgb_farben[hintergrundfarben[zeile, spalte]],
                                [spalte * 100 + 12, zeile * 100 + 12, 75, 75])

    for spalte in range(0, 5):  # Endwert exkludiert
        for zeile in range(0, 6):
            #pygame.Surface.fill(bildschirm, rgb_farben[hintergrundfarben[zeile, spalte]], [spalte * 100 + 12, runde * 100 + 12, 75, 75])
            pygame.draw.rect(bildschirm, rgb_farben["grau"], [spalte * 100 + 12, zeile * 100 + 12, 75, 75], 3,
                             5)  # 3 und 5 am Ende runden Vierecke ab
            buchstaben_text = schriftart.render(spielbrett[zeile][spalte], True, rgb_farben["schwarz"])
            bildschirm.blit(buchstaben_text, (spalte * 100+30, zeile * 100+25)) # Text erscheint auf Bildschirm
    pygame.draw.rect(bildschirm, rgb_farben["schwarz"], [position_zeile * 100 + 12, runde * 100 + 12, 75, 75], 3, 5)
    #pygame.draw.rect(bildschirm, gelb, [1 * 100 + 12, 0 * 100 + 12, 75, 75], 3,5)
    #pygame.draw.rect(bildschirm, rot, [2 * 100 + 12, 0 * 100 + 12, 75, 75], 3,5)


def buchstaben_einfaerben(eingabe, passwort) -> list[str]:
    if len(eingabe) != len (passwort):
        raise ValueError("Das eingegebene Wort muss genauso lang sein wie das Passwort")
    wortlaenge = len(passwort)
    eingabe_liste = list(eingabe.upper())
    #print(eingabe_liste)
    passwort_liste = list(passwort.upper())
    #print(passwort_liste)
    farben = [None] * wortlaenge  # erstellt leere Liste in der Länge des Worts
    gelbe_buchstaben = []  # leere Liste erstellen
    for i in range(0, wortlaenge):
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
        for i in range(wortlaenge - 1, -1, -1):  # Schleife rückwärts durch eingegebenes Wort
            if eingabe_liste[i] in gelb_mehrmals:
                if haeufigkeit_eingabe[eingabe_liste[i]] - anzahl_farbe_geaendert > haeufigkeit_passwort[
                    eingabe_liste[i]]:  # Buchstabe kommt häufiger im eingegebenen Wort vor als im Passwort
                    if farben[i] == 'gelb':  # es dürfen nur gelbe auf Rot gesetzt werden, keine grünen
                        farben[i] = 'rot'
                        anzahl_farbe_geaendert += 1

    #print(farben)
    return farben


spiel_aktiv = True
while spiel_aktiv:  # Spielschleife starten
    spiel_uhr.tick(bilder_pro_sekunde)
    bildschirm.fill(rgb_farben["weiss"])
    spielfeld_zeichnen()

    for ereignis in pygame.event.get():  # erlaubt es, über alle von pygame erkannten Ereignisse zu iterieren
        if ereignis.type == pygame.QUIT:  # Anweisung, um das Spielfenster zu schließen
            spiel_aktiv = False
            sys.exit()
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_BACKSPACE :
                if (spielbrett[runde][wortlaenge - 1] != ' ' ) & (wortlaenge - 1 == position_zeile) :#letztes Feld leer?
                    position_zeile = position_zeile
                elif position_zeile > 0 & (spielbrett[runde][wortlaenge - 1] == ' ' ):
                    position_zeile -= 1
                spielbrett[runde][position_zeile] = ' '
            if ereignis.key == pygame.K_DELETE :
                spielbrett[runde][position_zeile] = ' '
            if ereignis.key == pygame.K_RETURN and np.sum(spielbrett[runde,:] != " ") == 5: # Enter drücken, um in nächste Zeile zu gelangen
                eingabe = ("".join(spielbrett[runde][:wortlaenge]))
                print(eingabe)

                if eingabe not in wortliste:
                    meldung_anzeigen('Dein Wort ist ungültig!')
                    continue

                if scrabble_check(eingabe): # geprüftes Wort ist gültig
                    hintergrundfarben[runde,:] = buchstaben_einfaerben(eingabe, passwort)
                    spielfeld_zeichnen()
                    pygame.display.flip()
                    if passwort == ''.join(spielbrett[runde,:]): #Passwort erraten
                        print("gewonnen")
                        time.sleep(3)
                        spielende_anzeigen("Herzlichen Glückwunsch", "Du hast das Passwort erraten")
                        #bildschirm_gewonnen = pygame.display.set_mode((breite*1.5, hoehe/3))  # erstellt Spielfenster
                    if runde == anzahl_versuche - 1: #wort beim letzten Versuch nicht erraten
                        print("verloren")
                        time.sleep(3)
                        spielende_anzeigen("Du hast das Passwort leider nicht erraten", f"Das Passwort war {passwort.upper()}")
                    runde +=1
                anzahl_buchstaben = 0
                position_zeile = 0
            if ereignis.key == pygame.K_LEFT and position_zeile > 0:
                position_zeile -= 1
            if ereignis.key == pygame.K_RIGHT and position_zeile < wortlaenge - 1:
                position_zeile += 1

        if ereignis.type == pygame.TEXTINPUT:
            eingabe_zeichen = ereignis.__getattribute__('text').upper() # gibt ein Dictionary mit Attributen zurück
            print(eingabe_zeichen)
            if re.match(r"[A-Z]",eingabe_zeichen):
                spielbrett[runde][position_zeile] = eingabe_zeichen # aktuelle Runde und aktuelles Zeichen
                if position_zeile < wortlaenge - 1: # wenn nicht ganz rechts, dann einen Schritt nach rechts
                    position_zeile += 1
            print("anzahl buchstaben = ", np.sum(spielbrett[runde,:] != " "))

    pygame.display.flip()
pygame.quit()

