import numpy as np
import random
import re
import collections
import pygame
import Wort_in_scrabble_check
from Wort_in_scrabble_check import scrabble_check

pygame.init()

# screen setup
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
gruen = (0,204,0)
rot = (255, 0, 0)
gelb = (255, 255, 0)


rgb_farben = dict(weiss = (255, 255, 255), schwarz = (0, 0, 0), gruen = (0,204,0), rot = (255, 0, 0), gelb = (255, 255, 0), grau = (192, 192, 192))

screen_width = 500
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))  # create game window

turn = 0  # initialize turn variable
# create matrix
"""
board = [["", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", ""]]
"""

fps = 60 #frames per second
timer = pygame.time.Clock() #create clock object to control the frame rate
font = pygame.font.SysFont("freesensbold.ttf", 56)
wortlaenge = 5
anzahl_versuche = 6
hintergrundfarben = np.full((anzahl_versuche,wortlaenge),"weiss")

board = np.full((anzahl_versuche, wortlaenge), " ")

# Passwort aus Wortliste zufällig auswählen
wortliste = ['Apfel', 'Birne', 'Katze', 'Blume', 'Tisch', 'Stuhl', 'Lampe', 'Besen', 'Leine']
wortliste = [wort.upper() for wort in wortliste]
passwort = random.choice(wortliste).upper()
passwort_liste = list(passwort)
print(f"Das Passwort ist {passwort}")

#Initialbedingungen
letters = 0
turn = 0
turnactive = True #zu Beginn der Zeile haben wir weniger als 5 Buchstaben


def draw_board():
    global turn
    global board
    #for i in range (0,wortlaenge):
        #pygame.Surface.fill(screen, rgb_farben[hintergrundfarben[turn,i]], [i * 100 + 12, turn * 100 + 12, 75, 75])

    for col in range(0, 5):  # end value excluded
        for row in range(0, 6):
            pygame.Surface.fill(screen, rgb_farben[hintergrundfarben[row, col]],
                                [col * 100 + 12, row * 100 + 12, 75, 75])

    for col in range(0, 5):  # end value excluded
        for row in range(0, 6):
            #pygame.Surface.fill(screen, rgb_farben[hintergrundfarben[row, col]], [col * 100 + 12, turn * 100 + 12, 75, 75])
            pygame.draw.rect(screen, schwarz, [col * 100 + 12, row * 100 + 12, 75, 75], 3,
                             5)  # 3 and 5 at the end rounds rectangles
            piece_text = font.render(board[row][col], True, schwarz)
            screen.blit(piece_text, (col * 100+30, row * 100+25)) #draws text on the screen
    pygame.draw.rect(screen, rgb_farben["grau"], [letters * 100 + 12, turn * 100 + 12, 75, 75], 3,5)
    #pygame.draw.rect(screen, gelb, [1 * 100 + 12, 0 * 100 + 12, 75, 75], 3,5)
    #pygame.draw.rect(screen, rot, [2 * 100 + 12, 0 * 100 + 12, 75, 75], 3,5)


def buchstaben_faerben(eingabe, passwort, wortlaenge) -> list[str]:
    eingabe_liste = list(eingabe.upper())
    #print(eingabe_liste)
    passwort_liste = list(passwort.upper())
    #print(passwort_liste)
    farben = [None] * wortlaenge  # erstellt leere Liste in der Länge des Worts
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
        for i in range(wortlaenge - 1, -1, -1):  # schleife rückwärts
            if eingabe_liste[i] in gelb_mehrmals:
                if haeufigkeit_eingabe[eingabe_liste[i]] - anzahl_farbe_geaendert > haeufigkeit_passwort[
                    eingabe_liste[i]]:  # Buchstabe kommt häufiger im eingebenen Wort vor als im Passwort
                    if farben[i] == 'gelb':  # es dürfen nur gelbe auf Rot gesetzt werden keine grünen
                        farben[i] = 'rot'
                        anzahl_farbe_geaendert += 1

    print(farben)
    return farben


run = True
while run:  # initialize game loop
    timer.tick(fps)
    screen.fill(weiss)
    draw_board()

    for event in pygame.event.get():  # allows us to iterate over all the events that pygame picks up
        if event.type == pygame.QUIT:  # statement to close pygame window
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0: #wir können nur backspace drücken, wenn wir schon Buchstaben eingegeben haben
                board[turn][letters-1] = ''
                letters +=-1 #backspace zieht jeweils einen Buchstaben ab
            if event.key == pygame.K_RETURN and letters == 5: #enter drücken, um in nächste Zeile zu gelangen
                eingabe = ("".join(board[turn][:wortlaenge]))
                print(eingabe)
                if scrabble_check(eingabe): #wort ist gültig
                    hintergrundfarben[turn,:] = buchstaben_faerben(eingabe, passwort, wortlaenge)
                    print(hintergrundfarben)
                    turn +=1
                letters = 0

        if event.type == pygame.TEXTINPUT and turnactive:
            entry = event.__getattribute__('text') #gives dictionary of attribute
            print(event)
            if re.match(r"[A-Z]",entry.upper()):
                board[turn][letters] = entry.upper() #what turn and what letter we are on
                letters += 1

    if letters ==5: #end the turn
        turnactive = False
    if letters <5: #we can only add letters in this case
        turnactive = True

    pygame.display.flip()
pygame.quit()


