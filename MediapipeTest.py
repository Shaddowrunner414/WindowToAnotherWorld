import cv2
import mediapipe as mp
import pygame

# Initialisiere Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Bildschirmauflösung auslesen
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Starte die Webcam
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Die Webcam konnte nicht gestartet werden.")
            continue

        # Konvertiere das Bild von BGR nach RGB
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Verbessere die Leistung
        imageRGB.flags.writeable = False
        
        # Erkenne Gesichter
        results = face_detection.process(imageRGB)


        # Zeichne die Gesichtsboxen
        imageRGB.flags.writeable = True


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


        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            bestIdx = 0

            for detection in results.detections:
                #bestIdx finden
                pass

            mp_drawing.draw_detection(image, results.detections[bestIdx])
        

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Zeige das Bild an
        cv2.imshow('Gesichtserkennung', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Drücke ESC zum Beenden
            break

cap.release()
cv2.destroyAllWindows()
