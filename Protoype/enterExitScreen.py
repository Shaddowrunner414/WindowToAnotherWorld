import cv2
import mediapipe as mp
import time

class FaceCenterDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.quadrant_start_time = None
        self.quadrant_duration_threshold = 4  # seconds
        self.upper_right_triggered = False
        self.face_detected = False
        self.count = 0;

    def get_face_center(self, frame):
        # Convert the BGR image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process the image and track faces
        results = self.face_mesh.process(image)

        # Calculate the face center based on landmarks
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Initialize variables for calculating the center
                center_x = 0
                center_y = 0
                count = 0

                # Calculate the average of all landmark points to find the center
                for landmark in face_landmarks.landmark:
                    center_x += landmark.x
                    center_y += landmark.y
                    count += 1

                # Calculate the average
                center_x /= count
                center_y /= count

                # Convert coordinates to image size
                center_x = int(center_x * image.shape[1])
                center_y = int(center_y * image.shape[0])

                return center_x, center_y

        return None

    def check_upper_right_quadrant(self, center_x, center_y, frame_width, frame_height):
        if center_x > frame_width / 2 and center_y < frame_height / 2:
            if self.quadrant_start_time is None:
                self.quadrant_start_time = time.time()

            else:
                elapsed_time = time.time() - self.quadrant_start_time
                if elapsed_time >= self.quadrant_duration_threshold and not self.upper_right_triggered:
                    self.upper_right_triggered = True
                    
        else:
            if self.quadrant_start_time is not None and self.upper_right_triggered:
                # Preserve elapsed time
                self.quadrant_start_time = time.time() - self.quadrant_duration_threshold  


        if self.upper_right_triggered:
            self.count += 1
            print("Face detected in the upper right quadrant for at least 4 seconds for {} seconds".format(self.count))

    def process_frame(self, frame):
        face_center = self.get_face_center(frame)
        if face_center is not None:
            center_x, center_y = face_center
            self.check_upper_right_quadrant(center_x, center_y, frame.shape[1], frame.shape[0])
            if not self.face_detected:
                print("blinds open")
                self.face_detected = True
        else:
            if self.face_detected:
                print("blinds closed")
                self.face_detected = False
                # Reset the start time when no face is detected
                self.quadrant_start_time = None
                 # Reset trigger when no face is detected
                self.upper_right_triggered = False
                self.count = 0

    def close(self):
        self.face_mesh.close()

# Initialize the video capture object.
cap = cv2.VideoCapture(0)

try:
    face_detector = FaceCenterDetector()
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Process the frame to check face detection
        face_detector.process_frame(image)

        # Draw the face mesh annotations on the image.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = True

        results = face_detector.face_mesh.process(image)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                face_detector.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=face_detector.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=face_detector.drawing_spec,
                    connection_drawing_spec=face_detector.drawing_spec)

        # Display the image.
        cv2.imshow('MediaPipe FaceMesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

finally:
    face_detector.close()
    cap.release()
    cv2.destroyAllWindows()