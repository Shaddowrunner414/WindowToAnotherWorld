import cv2
import pygame
import sys
import os

# Pygame und OpenCV initialisieren
pygame.init()
cap = cv2.VideoCapture(0)  # 0 steht für die erste Kamera

# Gesichtserkennungs-Classifier laden
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Fenstergröße und Farben definieren
width = 1000
heigth = 800
fenster_groesse = (width, heigth)
schwarz = (0, 0, 0)
fenster = pygame.display.set_mode(fenster_groesse)
half_x = width * 0.2
half_y = heigth * 0.2

#Pfad des aktuellen Skripts ermittlen
script_dir = os.path.dirname(__file__)

#Relative Pfade für die Bilder festlegen
background_path = os.path.join(script_dir, "Background.png")
forground_path = os.path.join(script_dir, "Foreground.png")
middle_path = os.path.join(script_dir, "MiddleLayer.png")

# Bilder laden
hintergrund = pygame.image.load(background_path).convert()
vordergrund = pygame.image.load(forground_path).convert_alpha()
zwischenebene = pygame.image.load(middle_path).convert_alpha()  # Die dritte Ebene


# Anfangsposition der Bilder
x_vordergrund, y_vordergrund = half_x, half_y
x_zwischenebene, y_zwischenebene = half_x, half_y

#letze Erkannte Position
lastknown_x, lastknown_y = 0, 0

# Spiel-Schleife
running = True
while running:
    # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Kamerabild lesen
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Erstes erkanntes Gesicht verwenden, um die Position zu aktualisieren
    for (x, y, w, h) in faces:
        if lastknown_x !=0 and lastknown_y !=0:
            x_diff = x - lastknown_x
            y_diff = y - lastknown_y
            
            x_vordergrund += x_diff
            y_vordergrund -= y_diff #diese Zeile auskommentieren, wenn kein vertikales Tracking / Bewegung gewünscht

            # Bewege Middle Layer mit halber Geschwindigkeit
            x_zwischenebene += x_diff // 3
            y_zwischenebene -= y_diff // 3 #diese Zeile auskommentieren, wenn kein vertikales Tracking / Bewegung gewünscht

        lastknown_x, lastknown_y = x, y
        break  # Nur das erste Gesicht verwenden

    # Hintergrund und Vordergrund zeichnen
    fenster.fill(schwarz)
    fenster.blit(hintergrund, (0, 0))
    fenster.blit(zwischenebene, (x_zwischenebene, y_zwischenebene))
    fenster.blit(vordergrund, (x_vordergrund, y_vordergrund))
    
    # Fenster aktualisieren
    pygame.display.flip()

# Aufräumen
cap.release()
pygame.quit()
sys.exit()
