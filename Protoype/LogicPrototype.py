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
    return image

#Funktion um die Bilder zu skalieren und an die Bildschirmauflösung anzupassen
def load_and_scale(image_name, scale_factor=1.0):
    sf = scale_factor
    image = load(image_name)
    image_width = image.get_width()
    scale_factor = image_width / width 
    scale_factor2 = width / image_width
    print(scale_factor, scale_factor2, image_width, width)
    scaled_image = pygame.transform.scale(image, (image.get_width() * scale_factor2 * sf, image.get_height() * scale_factor2 * sf))
    image_width2 = scaled_image.get_width()
    image_height2 = scaled_image.get_height()
    print(image_width2, image_height2)
    return scaled_image

#Bilder laden
layer1 = load_and_scale("Background.png")
layer2 = load_and_scale("Foreground.png", scale_factor=0.2)

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
    window.blit(layer2, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Wenn die 'q'-Taste gedrückt wird
                running = False

# Aufräumen
cap.release()
pygame.quit()
sys.exit()