import random
import collections
import pygame

pygame.init()

# screen setup
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

screen_width = 500
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))  # create game window

turn = 0  # initialize turn variable
# create matrix
board = [["", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", ""]]

fps = 60 #frames per second
timer = pygame.time.Clock() #create clock object to control the frame rate
font = pygame.font.SysFont("freesensbold.ttf", 56)

# Passwort aus Wortliste zufällig auswählen
wortliste = ['Apfel', 'Birne', 'Katze', 'Blume', 'Tisch', 'Stuhl', 'Lampe', 'Besen', 'Leine']
wortliste = [wort.upper() for wort in wortliste]
passwort = random.choice(wortliste).upper()
passwort_liste = list(passwort)
print(f"Das Passwort ist {passwort}")

#Initialbedingungen
gameover = False
letters = 0
turnactive = True #zu Beginn der Zeile haben wir weniger als 5 Buchstaben


def draw_board():
    global turn
    global board
    for col in range(0, 5):  # end value excluded
        for row in range(0, 6):
            pygame.draw.rect(screen, white, [col * 100+12, row * 100+12, 75, 75], 3,
                             5)  # 3 and 5 at the end rounds rectangles
            piece_text = font.render(board[row][col], True, white)
            screen.blit(piece_text, (col * 100+30, row * 100+25)) #draws text on the screen
    pygame.draw.rect(screen, green,[5, turn*100+5, screen_width-10, 90], 3,5) #marks what line we are currently in



run = True
while run:  # initialize game loop
    timer.tick(fps)
    screen.fill(black)
    draw_board()


    for event in pygame.event.get():  # allows us to iterate over all the events that pygame picks up
        if event.type == pygame.QUIT:  # statement to close pygame window
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0: #wir können nur backspace drücken wenn wir schon Buchstaben eingegeben haben
                board[turn][letters-1] = ''
                letters +=-1 #backspace zieht jeweils einen Buchstaben ab
            if event.key == pygame.K_SPACE and not gameover: #space drücken um in nächste Zeile zu gelangen
                turn +=1
                letters = 0

        if event.type ==pygame.TEXTINPUT and turnactive and not gameover:
            entry =event.__getattribute__('text') #gives dictionary of attribute
            board[turn][letter] = entry #what turn and what letter we are on
            letters += 1


        if letters ==5: #end the turn
            turnactive = False
        if letters <5: #we can only add letters in this case
            turnactive = True

    pygame.display.flip()
pygame.quit()

###



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