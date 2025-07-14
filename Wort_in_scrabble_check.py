import ctypes
from multiprocessing import process
import subprocess

from pywinauto import Application
import pyautogui
import pytesseract
import time


#pfad_scrabble = r"C:\Users\isabe\3D Objects\MSc 4\Practical Python Development\projekt_passwort\SDeV-Turnier-Check_250501\SDeV-Check.exe"
pfad_scrabble = r"SDeV-Turnier-Check_250501/SDeV-Check.exe"

proc = subprocess.Popen([pfad_scrabble])
# Kurze Pause, um das Fenster in den Vordergrund zu bringen
time.sleep(1)

# Wort eingeben
#pyautogui.write("abcdefghi") #ungültiges Wort
pyautogui.write("fahrender") #gültiges Wort
time.sleep(1)

# Enter drücken
pyautogui.press('enter')


#app = Application(backend="uia").connect(title_re=".*")  # Passe den Fenstertitel an
app = Application(backend="uia").connect(process=proc.pid)

# Hole das Fenster
dlg = app.window(title_re=".*Scrabble.*")  # Versuche, mit allgemeinem Muster alle Fenster zu finden

#Position von Fenster 'SDeV Scrabble-Check 01.05.2025' berechnen
rect = dlg.rectangle()
print("Position (X, Y):", rect.left, rect.top)
# Breite und Höhe berechnen
width = rect.right - rect.left
height = rect.bottom - rect.top


screenshot = pyautogui.screenshot(region=(rect.left, rect.top , width, height))
screenshot_ausschnitt = pyautogui.screenshot(region=(int(1.2* rect.left), 2*rect.top , int(0.7*width), int(0.15 * height)))
#print(type(screenshot))
#screenshot.show()
screenshot_ausschnitt.show()
#screenshot_ausschnitt.save('screenshot_scrabble_existiert_nicht.jpg')

#text = pytesseract.image_to_string(screenshot)

#Funktion, dass er rot oder grün aus dem Screenshot erkennt
#wenns rot ist soll er neues wort eingeben
#wenn grün, Buchstabencheck und Prozess weiterdurchläuft

#Datei mit Scrabbel Liste