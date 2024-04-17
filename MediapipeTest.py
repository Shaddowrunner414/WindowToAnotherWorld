import cv2
import mediapipe as mp

# Initialisiere Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Starte die Webcam
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Die Webcam konnte nicht gestartet werden.")
            continue

        # Konvertiere das Bild von BGR nach RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Verbessere die Leistung
        image.flags.writeable = False
        
        # Erkenne Gesichter
        results = face_detection.process(image)

        # Zeichne die Gesichtsboxen
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            detection = results.detections[0]
            mp_drawing.draw_detection(image, detection)
        
        # Zeige das Bild an
        cv2.imshow('Gesichtserkennung', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Drücke ESC zum Beenden
            break

cap.release()
cv2.destroyAllWindows()