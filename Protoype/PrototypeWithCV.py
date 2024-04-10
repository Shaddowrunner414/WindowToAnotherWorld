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
ballon_path = os.path.join(script_dir, "hot-air-balloon.png")

#Funktion um Bilder zu laden und skalieren
def load_and_scale_image(image_path, scale_factor):
    image = pygame.image.load(image_path).convert_alpha()
    scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))
    return scaled_image


# Bilder laden und skalieren
hintergrund = load_and_scale_image(background_path, 1.0)
vordergrund = load_and_scale_image(forground_path, 0.5)
zwischenebene = load_and_scale_image(middle_path, 0.75)
ballon = load_and_scale_image(ballon_path, 0.3)



# Anfangsposition der Bilder
x_vordergrund, y_vordergrund = half_x, half_y
x_zwischenebene, y_zwischenebene = half_x, half_y
x_ballon, y_ballon = 2*half_x, 2*half_y

#letze Erkannte Position
lastknown_x, lastknown_y = half_x, half_y
lastknown_x2, lastknown_y2 = half_x, half_y
lastknown_x3, lastknown_y3 = half_x, half_y
#lastknown_x4, lastknown_y4 = 0, 0
#lastknown_x5, lastknown_y5 = 0, 0
#w, h = 170, 170
initialized = False
x_neu, y_neu = half_x, half_y


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
    if len(faces) > 0:  # Ensure faces is not empty
        (x, y, w_face, h_face) = faces[0]  # Only the first detected face
        if not initialized:
            w, h = w_face, h_face
            initialized = True

        #if(abs(x-lastknown_x > 50)):
       #     x = lastknown_x3
            
        #if(abs(y-lastknown_y > 50)):
       #     y = lastknown_y3

        #if lastknown_x != 0 and lastknown_y != 0: #??
        x_neu = ((x + lastknown_x*9)/10)
        y_neu = ((y + lastknown_y*9)/10)

        print("x: ", x,  "y: ", y)

        x_vordergrund = x_neu
        y_vordergrund = y_neu # diese Zeile auskommentieren, wenn kein vertikales Tracking / Bewegung gewünscht

        # Bewege Middle Layer mit halber Geschwindigkeit
        # x_zwischenebene += x_diff / 3
        # y_zwischenebene -= y_diff / 3  # diese Zeile auskommentieren, wenn kein vertikales Tracking / Bewegung gewünscht

        # Bewege Ballon
        # x_ballon += x_diff // 2  # auskommentiert weil nur vertikal gewünscht
        # y_ballon += y_diff / 2

        lastknown_x, lastknown_y = x_neu, y_neu
        lastknown_x2, lastknown_y2 = lastknown_x, lastknown_y
        lastknown_x3, lastknown_y3 = lastknown_x2, lastknown_y2
        #lastknown_x4, lastknown_y4 = lastknown_x3, lastknown_y3
        #lastknown_x5, lastknown_y5 = lastknown_x4, lastknown_y4

    # Hintergrund und Vordergrund zeichnen
    fenster.fill(schwarz)
    fenster.blit(hintergrund, (0, 0))
    fenster.blit(zwischenebene, (x_zwischenebene, y_zwischenebene))
    fenster.blit(vordergrund, (x_vordergrund, y_vordergrund)) # koordinaten runden auf ganze Zahlen
    fenster.blit(ballon, (x_ballon, y_ballon))
    
    # Fenster aktualisieren
    pygame.display.flip()

# Aufräumen
cap.release()
pygame.quit()
sys.exit()
