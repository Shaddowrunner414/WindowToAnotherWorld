import cv2
import mediapipe as mp
#from main import lastknown_x, lastknown_y

# class FaceDetector:
#     def __init__(self):
#         self.face_detection = mp.solutions.face_detection.FaceDetection()
#         self.drawing = mp.solutions.drawing_utils

#     def process_frame(self, frame):
#         # Convert the BGR image to RGB
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Process the frame
#         results = self.face_detection.process(rgb_frame)

#         # If faces are detected
#         if results.detections:
#             for detection in results.detections:
#                 # Get the bounding box
#                 box = detection.location_data.relative_bounding_box
#                 h, w, _ = frame.shape
#                 xmin = int(box.xmin * w)
#                 ymin = int(box.ymin * h)
#                 xmax = int(xmin + box.width * w)
#                 ymax = int(ymin + box.height * h)

#                 # Calculate the center of the face
#                 face_x_center = (xmin + xmax) // 2
#                 face_y_center = (ymin + ymax) // 2

#                 # Motion smoothing of the face to make the movement of the layers more continuous and less jerky
#                 #smooth_face_x_center = (face_x_center + lastknown_x * 9) // 10 # Clarification if needed
#                 #smoot_face_y_center = (face_y_center + lastknown_y * 9) // 10         
            

#                 #return smooth_face_x_center, smoot_face_y_center
#                 return face_x_center, face_y_center