import pytest
#from Wort_in_scrabble_check import scrabble_check
from buchstaben_einfarben import buchstaben_einfaerben
from buchstaben_einfarben import ist_wort_erlaubt


def test_scrabble_check():
    assert scrabble_check("in")
    assert scrabble_check("Schramme")
    assert scrabble_check("Katze")
    assert scrabble_check("Frage")
    assert not scrabble_check("ii")
    assert not scrabble_check("wwwwwwwww")
    assert not scrabble_check("Asien")

def test_buchstaben_einfarben():
    assert buchstaben_einfaerben("Kater","Katze") == ["gruen", "gruen", "gruen", "gelb", "rot"]
    assert buchstaben_einfaerben("leben","Klebe") == ["gelb", "gelb", "gelb", "gelb", "rot"]
    assert buchstaben_einfaerben("Kleie", "Stein") == ["rot", "rot", "gruen", "gruen", "rot"]
    assert buchstaben_einfaerben("Mütze", "Münze") == ["gruen", "gruen", "rot", "gruen", "gruen"]
    assert not buchstaben_einfaerben("Müsli", "Löwen") == ["rot", "rot", "rot", "rot", "rot"]
    with pytest.raises(ValueError): buchstaben_einfaerben("Kate", "Katze") # Buchstabenanzahl ungleich


def test_ist_wort_erlaubt():
    assert ist_wort_erlaubt("Katze")
    assert ist_wort_erlaubt("Asiat")
    assert not ist_wort_erlaubt("Asien")
    assert not ist_wort_erlaubt("abcde")
    assert ist_wort_erlaubt("Wüste")
    assert ist_wort_erlaubt("Ziege")
