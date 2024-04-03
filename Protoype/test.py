import cv2
import pygame
import sys
import os

# Pygame und OpenCV initialisieren
pygame.init()
cap = cv2.VideoCapture(0)  # 0 steht für die erste Kamera

# Gesichtserkennungs-Classifier laden
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Bildschirmauflösung auslesen
info = pygame.display.Info()
width, heigth = info.current_w, info.current_h

#Hintergrund-Canvas-Farbe definieren
black = (0, 0, 0)

#Fenster und Mittelpunkt definieren
window = pygame.display.set_mode((width, heigth), pygame.FULLSCREEN)
x_center = width // 2
y_center = heigth // 2 


#Pfad des aktuellen Skripts ermittlen
script_dir = os.path.dirname(__file__)

#Funktion um die Bilder mit relativen Pfaden zu laden
def load(image_name):
    image = pygame.image.load(os.path.join(script_dir, image_name)).convert_alpha()
    print(int(image.get_width()))
    return image

#Funktion um die Bilder zu skalieren und an die Bildschirmauflösung anzupassen
def load_and_scale(image_name):
    image = load(image_name)

    scale_factor = 0.5
    scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))
    return scaled_image

#Bilder laden
layer1 = load_and_scale("Background.png")

#Anfangsposition der Bilder

#Spiel-Schleife
running = True
while running:
      # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hintergrund und Vordergrund zeichnen
    window.fill(black)
    window.blit(layer1, (0, 0))

    pygame.display.flip()

# Aufräumen
cap.release()
pygame.quit()
sys.exit()