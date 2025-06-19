import numpy as np
import random

wortliste = ['Apfel', 'Birne', 'Katze', 'Blume', 'Tisch', 'Stuhl', 'Lampe']
random.choice(wortliste)
print(random.choice(wortliste))

wort = input("Gib ein Wort ein: ")
print("Du hast das Wort eingegeben:", wort)

print (wort in wortliste)
if (wort in wortliste): 
    print("Das Wort ist in der Liste!")
else: 
    (print("Das Wort ist nicht in der Liste!"))
