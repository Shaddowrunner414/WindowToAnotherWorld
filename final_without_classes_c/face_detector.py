import time
import cv2
import mediapipe as mp
from layer_adjustment import ballon_speed_up

class FaceCenterDetector:
    # Initialize the FaceCenterDetector
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        
        # Initialize MediaPipe FaceMesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1, # Detect only one face
            refine_landmarks=True, # use the extended 468 landmark model
            min_detection_confidence=0.5, # Mimimum confidence for face detection
            min_tracking_confidence=0.5 # Minimum confidence for landmark tracking
        )

        # Initialize timing and state variables
        self.quadrant_start_time = None
        self.quadrant_duration_threshold = 2  # seconds
        self.upper_right_triggered = False
        self.face_detected = False
        self.count = 0 # Strutz wozu?? #Jonas: ich glaube zum debugging. 
        self.last_face_detected_time = None
        self.last_face_lost_time = None

    # Detect a face in a given frame and calculate its center point
    def get_face_center(self, image):

        # To improve performance, optionally mark the image as not writable to pass by reference instead of copying
        image.flags.writeable = False

        # Process the image and detect faces
        results = self.face_mesh.process(image)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Calculate the average position of all landmarks
                center_x = sum(landmark.x for landmark in face_landmarks.landmark) / len(face_landmarks.landmark)
                center_y = sum(landmark.y for landmark in face_landmarks.landmark) / len(face_landmarks.landmark)
                
                # Return the normalized coordinates (values between 0 and 1)
                return center_x, center_y
                
                # deprecated
                # just return the center x/y and multiply it with the resolution in main.py
                # landx = face_landmarks.landmark[0].x
                # landy = face_landmarks.landmark[0].y
                #return int(center_x * image.shape[1]), int(center_y * image.shape[0])
        # Return None if no face is detected
        return None

    
    """
    Check if the detected face is in the upper right quadrant of the frame.
    Also monitor how long the face stays in the upper right quadrant and trigger an action if it stays there for a specified duration
    """
    def check_upper_right_quadrant(self, center_x, center_y, frame_width, frame_height):
        
        ballon_offset_flag = 0 # Strutz
        #Check if the face is in the upper right quadrant
        if 2 * center_x > frame_width and 2 * center_y > frame_height:
            if self.quadrant_start_time is None:
                # Start timing when face enters the quadrant
                self.quadrant_start_time = time.time()
            else:
                # Check how long the face has been in the quadrant
                elapsed_time = time.time() - self.quadrant_start_time
                # ballon_speed_up() Strutz
                if elapsed_time >= self.quadrant_duration_threshold:
                    ballon_offset_flag = 1 # Strutz
                # if elapsed_time >= self.quadrant_duration_threshold and not self.upper_right_triggered:
                #     # Trigger the action if the threshold is reached
                #     self.upper_right_triggered = True
        else:
            # Reset timing if face leaves the quadrant, but keep triggered state
            if self.quadrant_start_time is not None and self.upper_right_triggered:
                self.quadrant_start_time = time.time() - self.quadrant_duration_threshold  
        
        # Increment count if action is triggered (used of debugging and testing)
        if self.upper_right_triggered:
            self.count += 1 # Strutz wozu?? #Jonas: genau wie oben: debug
        return ballon_offset_flag

    """
    Process a frame to detect a face and control the curtains 
    """
    def process_frame(self, frame):

        # Gather the coordinates of the center of the face
        face_center = self.get_face_center(frame)
        current_time = time.time()

        if face_center is not None:
            center_x, center_y = face_center
            
            # Check if a face is in the upper right quadrant
            self.check_upper_right_quadrant(center_x, center_y, frame.shape[1], frame.shape[0])
            
            if not self.face_detected:
                if self.last_face_detected_time is None:

                    # Start timing when a face is detected
                    self.last_face_detected_time = current_time
                elif current_time - self.last_face_detected_time >= 1:
                    # If a face as been consistently detected for 2 seonds open the curtains
                    #print("curtains open")
                    self.face_detected = True
                    self.last_face_detected_time = None
        else:
            if self.face_detected:
                if self.last_face_lost_time is None:

                    # Start timing when the face is lost
                    self.last_face_lost_time = current_time
                elif current_time - self.last_face_lost_time >= 1:
                    
                    # If no face has been detected for 2 seconds, close the curtains
                    #print("curtains closed")
                    self.face_detected = False
                    self.last_face_lost_time = None
                    self.quadrant_start_time = None
                    self.upper_right_triggered = False
                    self.count = 0 # Strutz wozu?? #Jonas: genau wie oben: debug

    # Release resources used by the FaceMesh object
    # Should be called when the FaceCenterDetector is no longer needed
    def close(self):
        self.face_mesh.close()