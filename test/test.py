import pytest
from src.funktionen_play_passwort import buchstaben_einfaerben
from src.funktionen_play_passwort import ist_wort_erlaubt

def test_buchstaben_einfarben():
    assert buchstaben_einfaerben("Kater","Katze") == ["gruen", "gruen", "gruen", "gelb", "rot"]
    assert buchstaben_einfaerben("leben","Klebe") == ["gelb", "gelb", "gelb", "gelb", "rot"]
    assert buchstaben_einfaerben("Kleie", "Stein") == ["rot", "rot", "gruen", "gruen", "rot"]
    assert buchstaben_einfaerben("Mütze", "Münze") == ["gruen", "gruen", "rot", "gruen", "gruen"]
    assert not buchstaben_einfaerben("Müsli", "Löwen") == ["rot", "rot", "rot", "rot", "rot"]
    with pytest.raises(ValueError):
        buchstaben_einfaerben("Kate", "Katze") # Buchstabenanzahl ungleich


def test_ist_wort_erlaubt():
    assert ist_wort_erlaubt("Katze")
    assert ist_wort_erlaubt("Asiat")
    assert not ist_wort_erlaubt("Asien")
    assert not ist_wort_erlaubt("abcde")
    assert ist_wort_erlaubt("Wüste")
    assert ist_wort_erlaubt("Ziege")
