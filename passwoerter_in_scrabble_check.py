from Wort_in_scrabble_check import scrabble_check

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

for wort in wortliste:
    if not scrabble_check(wort):
        print(wort, "ist bei Scrabble nicht erlaubt")
