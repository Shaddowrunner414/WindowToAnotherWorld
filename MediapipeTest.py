import cv2
import mediapipe as mp

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Start the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for tracking
prev_detection = None

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Die Webcam konnte nicht gestartet werden.")
            continue

        # Convert the image from BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        results = face_detection.process(image_rgb)

        if results.detections:
            # Choose the largest face detected
            largest_detection = max(results.detections, key=lambda det: det.location_data.relative_bounding_box.width * det.location_data.relative_bounding_box.height)

            # Track the largest face
            if prev_detection is None:
                prev_detection = largest_detection
            else:
                prev_center_x = prev_detection.location_data.relative_bounding_box.xmin + prev_detection.location_data.relative_bounding_box.width / 2
                prev_center_y = prev_detection.location_data.relative_bounding_box.ymin + prev_detection.location_data.relative_bounding_box.height / 2
                curr_center_x = largest_detection.location_data.relative_bounding_box.xmin + largest_detection.location_data.relative_bounding_box.width / 2
                curr_center_y = largest_detection.location_data.relative_bounding_box.ymin + largest_detection.location_data.relative_bounding_box.height / 2

                # Check if the distance between centers is small enough to consider it the same face
                distance_threshold = 0.1  # Adjust as needed
                distance = ((prev_center_x - curr_center_x) ** 2 + (prev_center_y - curr_center_y) ** 2) ** 0.5
                if distance < distance_threshold:
                    prev_detection = largest_detection

            # Draw bounding box
            mp_drawing.draw_detection(image, prev_detection)

        # Show the image
        cv2.imshow('Gesichtserkennung', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit
            break

cap.release()
cv2.destroyAllWindows()