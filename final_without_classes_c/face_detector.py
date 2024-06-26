import time
import cv2
import mediapipe as mp

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
        self.count = 0
        self.last_face_detected_time = None
        self.last_face_lost_time = None

    def get_face_center(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.face_mesh.process(image)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                center_x = sum(landmark.x for landmark in face_landmarks.landmark) / len(face_landmarks.landmark)
                center_y = sum(landmark.y for landmark in face_landmarks.landmark) / len(face_landmarks.landmark)
                return int(center_x * image.shape[1]), int(center_y * image.shape[0])
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
                self.quadrant_start_time = time.time() - self.quadrant_duration_threshold  

        if self.upper_right_triggered:
            self.count += 1

    def process_frame(self, frame):
        face_center = self.get_face_center(frame)
        current_time = time.time()

        if face_center is not None:
            center_x, center_y = face_center
            self.check_upper_right_quadrant(center_x, center_y, frame.shape[1], frame.shape[0])
            
            if not self.face_detected:
                if self.last_face_detected_time is None:
                    self.last_face_detected_time = current_time
                elif current_time - self.last_face_detected_time >= 2:
                    print("blinds open")
                    self.face_detected = True
                    self.last_face_detected_time = None
        else:
            if self.face_detected:
                if self.last_face_lost_time is None:
                    self.last_face_lost_time = current_time
                elif current_time - self.last_face_lost_time >= 2:
                    print("blinds closed")
                    self.face_detected = False
                    self.last_face_lost_time = None
                    self.quadrant_start_time = None
                    self.upper_right_triggered = False
                    self.count = 0

    def close(self):
        self.face_mesh.close()