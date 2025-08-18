from collections import Counter
import cv2
import numpy as np
import  keyboard
import  re
import subprocess
import psutil
from pywinauto import Application
import pyautogui
import time
import Screenshot_farbe_erkennen
from Screenshot_farbe_erkennen import ist_wort_erlaubt_screenshot


def scrabble_check(wort: str) -> bool:

    #Scrabble Check öffnen
    pfad_scrabble = r"Scrabbel Wort Check\SDeV- Check.exe"
    proc = subprocess.Popen(pfad_scrabble)
    #Tastatur sperren
    for i in range(150):
        keyboard.block_key(i)
    # Kurze Pause, um das Fenster in den Vordergrund zu bringen
    time.sleep(1)

    # Wort eingeben
    #pyautogui.write("ii") #ungültiges Wort
    #pyautogui.write("hammer") #gültiges Wort
    pyautogui.write(wort) #übergebener Parameter
    #time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    #Verbinden mit Scrabble Wort Check
    app = Application(backend="uia").connect(process=proc.pid)

    # Hole das Fenster
    dlg = app.window(title_re=".*Scrabble.*")

    #Position von Fenster 'SDeV Scrabble-Check 01.05.2025' berechnen
    rect = dlg.rectangle()
    #print("Position (X, Y):", rect.left, rect.top)
    # Breite und Höhe berechnen
    width = int((rect.right - rect.left)*0.85)
    height = int((rect.bottom - rect.top)*0.55)


    screenshot_ausschnitt = pyautogui.screenshot(region=(rect.left, rect.top , width, height))
    ##screenshot_ausschnitt = pyautogui.screenshot(region=(int(1.2* rect.left), 2*rect.top , int(0.7*width), int(0.15 * height)))
    #print(type(screenshot_ausschnitt))
    #screenshot.show()
    #screenshot_ausschnitt.show()
    screenshot_ausschnitt.save('screenshot_scrabble.jpg')
    for i in range(150):
        keyboard.unblock_key(i)
    proc.terminate()

    return ist_wort_erlaubt_screenshot('screenshot_scrabble.jpg')
#scrabble_check("ist")