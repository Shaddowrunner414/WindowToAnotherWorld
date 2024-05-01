import pyrealsense2 as rs
import numpy as np  
import cv2
import mediapipe as mp


#class CameraManager:

# Liste alle verfügbareren RealSense-Geräte
context = rs.context()
device_list = context.query_devices()
realsense_devices = {device.get_info(rs.camera_info.name): device.get_info(rs.camera_info.serial_number) for device in device_list}

# Wähle die gewünschte Kamera
device_id = "Intel RealSense D435" 

# Starte die Kamera
if isinstance(device_id, int):
    cap = cv2.VideoCapture(device_id)
else:
    pipeline = rs.pipeline()
    config = rs.config()
    if device_id in realsense_devices:
        config.enable_device(realsense_devices[device_id])
    config.enable_stream(rs.stream.depth)
    config.enable_stream(rs.stream.color)
    pipeline.start(config)

# Initialisiere Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


try:
    while True:
        if isinstance(device_id, int):
            ret, frame = cap.read()
            if not ret:
                break
            color_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            frames = pipeline.wait_for_frames()
            aligned_frames = rs.align(rs.stream.color).process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

            # Generiere eine einfache Vordergrundmaske
            threshold = 1.5  # Schwellenwert in Metern
            depth_scale = pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
            threshold = threshold / depth_scale
            foreground_mask = np.where((depth_image > 0) & (depth_image < threshold), 255, 0).astype(np.uint8)

            # Wende die Maske auf das Farbbild an, um den Vordergrund zu extrahieren
            foreground_image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask=foreground_mask)

            # Erkenne Gesichter im Bild ohne Hintergrund
            results = face_detection.process(foreground_image)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(foreground_image, detection)


finally:
    if isinstance(device_id, int):
        cap.release()
    else:
        pipeline.stop()
    cv2.destroyAllWindows()