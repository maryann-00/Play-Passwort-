from collections import Counter
import cv2
import numpy as np

def ist_wort_erlaubt_screenshot(dateipfad: str) -> bool:
    maske_gruen = farbmaske_berechnen("gruen", dateipfad)
    anteil_gruen = maske_gruen["farbig"]/maske_gruen["schwarz"]
    maske_rot = farbmaske_berechnen("rot", dateipfad)
    anteil_rot = maske_rot["farbig"]/maske_gruen["schwarz"]
    return anteil_gruen >= anteil_rot


def farbmaske_berechnen(farbe: str, dateipfad: str) -> dict[str,int]:
    if farbe == "gruen":
        untergrenze = (39, 50, 25)  # untere Grenze grün in HSV
        obergrenze = (80, 255, 255)  # obere Grenze grün in HSV
        hsv_grenzen = (untergrenze, obergrenze)
    elif farbe == "rot":
        untergrenze = (140, 29, 0)  # untere Grenze rot in HSV
        obergrenze = (179, 255, 255)  # obere Grenze rot in HSV
        hsv_grenzen = (untergrenze, obergrenze)
    else :
        raise(ValueError("Es sind nur die Farben rot und gruen erlaubt"))


    untergrenze = hsv_grenzen[0]
    obergrenze = hsv_grenzen[1]
    img = cv2.imread(dateipfad)
    #print(type(img))
    cv2.imshow('Original Image', img)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow('hsv_img', hsv_img)

    maske = cv2.inRange(hsv_img, untergrenze, obergrenze)  # 0 für Schwarz, 255 für farbe
    color_image = cv2.bitwise_and(img, img, mask=maske)
    #cv2.imshow('Coloured Image', color_image)
    cv2.waitKey(0)
    #print(type(maske))
    counter_pixel_farbe = Counter(maske.flatten())# 0 für Schwarz, 255 für farbige
    #print(counter_pixel_farbe)
    #print(counter_pixel_farbe[0],counter_pixel_farbe[255])
    return { 'farbig': counter_pixel_farbe[255], 'schwarz': counter_pixel_farbe[0]}



print(ist_wort_erlaubt_screenshot(r'C:\Users\isabe\PycharmProjects\Play-Passwort-\screenshot_scrabble.jpg'))