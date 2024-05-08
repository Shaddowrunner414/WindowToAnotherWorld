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

    def get_face_center(self, frame):
        # Convert the BGR image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process the image and track faces
        results = self.face_mesh.process(image)

        # calculate the face center based on landmarks
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

                # Motion smoothing of the face to make the movement of the layers more continuous and less jerky
                #smooth_center_x = (center_x + lastknown_x * 9) // 10 # Clarification if needed
                #smoot_center_y = (center_y + lastknown_y * 9) // 10 

                return center_x, center_y

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

        # Get the face center coordinates
        face_center = face_detector.get_face_center(image)
        if face_center is not None:
            center_x, center_y = face_center
            print("Face center coordinates:", center_x, center_y)
            # Process the image and track faces
            results = face_detector.face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = True

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