import cv2
import pygame
import sys

# Pygame und OpenCV initialisieren
pygame.init()
cap = cv2.VideoCapture(0)  # 0 steht für die erste Kamera

# Gesichtserkennungs-Classifier laden
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Fenstergröße und Farben definieren
fenster_groesse = (640, 480)
schwarz = (0, 0, 0)
fenster = pygame.display.set_mode(fenster_groesse)

# Bilder laden
hintergrund = pygame.image.load("Background.png").convert()
vordergrund = pygame.image.load("Foreground.png").convert_alpha()
zwischenebene = pygame.image.load("MiddleLayer.png").convert_alpha()  # Die dritte Ebene


# Anfangsposition des Vordergrundbildes
x_vordergrund, y_vordergrund = 50, 100

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
        x_vordergrund = x - w // 2
        y_vordergrund = y - h // 2
        break  # Nur das erste Gesicht verwenden

    # Hintergrund und Vordergrund zeichnen
    fenster.fill(schwarz)
    fenster.blit(hintergrund, (0, 0))
    fenster.blit(vordergrund, (x_vordergrund, y_vordergrund))
    
    # Fenster aktualisieren
    pygame.display.flip()

# Aufräumen
cap.release()
pygame.quit()
sys.exit()
