import dlib
import cv2
import numpy as np

# Initialize face detector and tracker
detector = dlib.get_frontal_face_detector()
tracker = dlib.correlation_tracker()

# Read the input video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = detector(gray)
    
    # Iterate through detected faces
    for face in faces:
        # Get face coordinates
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        
        # Initialize the tracker with the current frame and face bounding box
        tracker.start_track(frame, dlib.rectangle(x, y, x+w, y+h))

        # Draw rectangle without dlib
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Update the tracker to track the face
        tracker.update(frame)
        
        # Get the updated position of the tracked face
        pos = tracker.get_position()
        x1, y1 = int(pos.left()), int(pos.top())
        x2, y2 = int(pos.right()), int(pos.bottom())
        
        # Draw rectangle around the tracked face
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        
    

    # Display the output frame
    cv2.imshow('Face Tracking', frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
