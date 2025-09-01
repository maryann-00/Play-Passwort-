import pytest
import Wort_in_scrabble_check
from Wort_in_scrabble_check import scrabble_check
#from 'Play Passwort' import richtige_wortlaenge


def test_scrabble_check():
    assert scrabble_check("in")
    assert scrabble_check("Schramme")
    assert scrabble_check("Katze")
    assert scrabble_check("Frage")
    assert not scrabble_check("ii")
    assert not scrabble_check("wwwwwwwww")
    assert not scrabble_check("Asien")

#def test_richtige_wortlaenge()
    #assert richtige_wortlaenge(katze,5)
    #assert not richtige_wortlaenge(katze,6)

