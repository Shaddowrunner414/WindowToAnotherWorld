import cv2
import pygame
import sys
import os
import mediapipe as mp
import ctypes

# Initialisiere Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Pygame und OpenCV initialisieren
pygame.init()
cap = cv2.VideoCapture(0)  # 0 steht für die erste Kamera

# Gesichtserkennungs-Classifier laden
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#Systemsskalierung auslesen
scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
print("\nSkalierung: ", scaleFactor)
sysSf = scaleFactor

#Bildschirmskalierung von pygame ausgeben(Standartmäßig 96 dpi)
def get_system_scaling():
    try:
        user32 = ctypes.windll.user32
        # Horizontale Skalierungsfaktor abrufen
        h_scale = user32.GetDpiForSystem()
        # Vertikale Skalierungsfaktor abrufen
        v_scale = user32.GetDpiForSystem()
        return h_scale, v_scale
    except Exception as e:
        print("Fehler beim Abrufen der Systemskalierung:", str(e))
        return None, None

# Systemskalierung auslesen
horizontal_scale, vertical_scale = get_system_scaling()
if horizontal_scale is not None and vertical_scale is not None:
    print("Horizontale Systemskalierung:", horizontal_scale)
    print("Vertikale Systemskalierung:", vertical_scale)

pyScale = 100/vertical_scale    

# Bildschirmauflösung auslesen
info = pygame.display.Info()
width, height = info.current_w, info.current_h
print("Bildschirmauflösung Breite: ", width, "Bildschirmauflösung Höhe: ",  height)

#Hintergrund-Canvas-Farbe definieren
black = (0, 0, 0)

#Fenster und Mittelpunkt definieren
window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
x_starter = width * 0.2
y_starter = height * 0.2 

#Pfad des aktuellen Skripts ermittlen
script_dir = os.path.dirname(__file__)

#Funktion um die Bilder mit relativen Pfaden zu laden
def load(image_name):
    image = pygame.image.load(os.path.join(script_dir, image_name)).convert_alpha()
    return image

#Funktion um die Bilder zu skalieren und an die Bildschirmauflösung anzupassen
def load_and_scale(image_name, scale_factor=1.0):
    print("__")
    sf = scale_factor
    image = load(image_name)
    image_width = image.get_width()
    image_height = image.get_height()
    scale_factor = height / image_height 
    scale_factor2 = width / image_width

    #Automatisches Skalieren
    if image_width > image_height:
        scaled_image = pygame.transform.scale(image, (image.get_width() * scale_factor2 * sf, image.get_height() * scale_factor2 * sf))
        image_width2 = scaled_image.get_width()
        image_height2 = scaled_image.get_height()
        print("W>H", scale_factor2, image_width, image_width2, width, image_height, image_height2, height, image_name)
    elif image_width <= image_height:
        scaled_image = pygame.transform.scale(image, (image.get_width() * scale_factor * sf, image.get_height() * scale_factor * sf))
        image_width2 = scaled_image.get_width()
        image_height2 = scaled_image.get_height()
        print("W<H", scale_factor, image_width, image_width2, width, image_height, image_height2, height, image_name)

    #image_width2 = scaled_image.get_width()
    #image_height2 = scaled_image.get_height()
    #print(scale_factor, scale_factor2, image_width, width, image_width2, image_height2, image_name)
    print("__")
    return scaled_image

#Bilder laden
#Layer Index zählt vom Hintergrund beginnend aus hoch
if sysSf == 1.25:
    layer1 = load_and_scale("canada.png", scale_factor=pyScale)
    layer2 = load_and_scale("Foreground.png", scale_factor=0.2)
elif sysSf != 1.25:    
    layer1 = load_and_scale("canada.png")
    layer2 = load_and_scale("Foreground.png", scale_factor=0.2)

#Anfangsposition der Bilder
x_layer1, x_layer2 = x_starter, x_starter
y_layer1, y_layer2 = y_starter, y_starter


#letzte bekannte Position
lastknown_x, lastknown_y = x_starter, y_starter


#Spiel-Schleife
running = True
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while running:
        success, image = cap.read()
        if not success:
            print("Die Webcam konnte nicht gestartet werden")
            continue

        # Ereignisse prüfen (z.B. Tasteninput für quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Konvertiere das Bild von BGR nach RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Verbessere die Leistung
        #image.flags.writeable = False

        # Erkenne Gesichter
        results = face_detection.process(image)

        # Initialisiere diese Variablen
        x_face_now, y_face_now = width * 0.2, height * 0.2  


        # Koordinaten des Gesichts auslesen und motion smoothing anwenden
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x_face_now = int(bbox.xmin * width)
                y_face_now = int(bbox.ymin * height)
                lastknown_x = (x_face_now + lastknown_x * 9) / 10
                lastknown_y = (y_face_now + lastknown_y * 9) / 10
        else:
            lastknown_x = (lastknown_x * 9) / 10
            lastknown_y = (lastknown_y * 9) / 10

        print("x: ", x_face_now, "y: ", y_face_now)

        #motion smoothing um Bewegung der Ebenen kontinuierlicher und weniger sprunghaft zu gestalten
        x_neu = ((x_face_now + lastknown_x*9)/10)
        y_neu = ((y_face_now + lastknown_y*9)/10)

        #layer bewegen
        x_layer2 = x_neu
        y_layer2 = y_neu






        # Hintergrund und Vordergrund zeichnen
        window.fill(black)
        window.blit(layer1, (0, 0))
        window.blit(layer2, (x_layer2, y_layer2))

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