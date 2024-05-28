import cv2
import pygame
import sys
import os
import mediapipe as mp
import pyrealsense2 as rs
import numpy as np
import ctypes

# AssetManager class to manage the threshold value
class AssetManager:
    background_removal_threshold = 1.0  # Adjust this value as needed

# CameraManager class to manage RealSense camera operations
class CameraManager:
    def __init__(self, device_id):
        self.device_id = device_id
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # List all available RealSense devices
        context = rs.context()
        device_list = context.query_devices()
        realsense_devices = {device.get_info(rs.camera_info.name): device.get_info(rs.camera_info.serial_number) for device in device_list}

        # Configure and start the RealSense camera
        if device_id in realsense_devices:
            self.config.enable_device(realsense_devices[device_id])  # Use the serial number
        self.config.enable_stream(rs.stream.depth)
        self.config.enable_stream(rs.stream.color)

    def start(self):
        self.pipeline.start(self.config)

    def stop(self):
        self.pipeline.stop()    

    def get_frame(self):
        # Wait for a coherent set of frames: a color frame and a depth frame
        frames = self.pipeline.wait_for_frames()
        aligned_frames = rs.align(rs.stream.color).process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Convert images to NumPy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Convert the BGR image to an RGB image
        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Generate a simple foreground mask by ignoring all depth values that are above a threshold
        depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        threshold = AssetManager.background_removal_threshold / depth_scale
        foreground_mask = np.where((depth_image > 0) & (depth_image < threshold), 255, 0).astype(np.uint8)

        # Apply the mask to the color image to extract the foreground
        foreground_image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask=foreground_mask)

        return color_image_rgb, foreground_image

# FaceCenterDetector class for face center detection
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
                center_x = int(center_x * frame.shape[1])
                center_y = int(center_y * frame.shape[0])

                return center_x, center_y

    def close(self):
        self.face_mesh.close()

# Initialize Pygame
pygame.init()

# Initialize RealSense CameraManager
camera = CameraManager(device_id="YourDeviceID")  # Set your actual device ID
camera.start()

# Initialize FaceCenterDetector
face_detector = FaceCenterDetector()

# Read system scaling
scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
print("\nScaling: ", scaleFactor)
sysSf = scaleFactor

# Get system scaling for Pygame (default 96 dpi)
def get_system_scaling():
    try:
        user32 = ctypes.windll.user32
        h_scale = user32.GetDpiForSystem()
        v_scale = user32.GetDpiForSystem()
        return h_scale, v_scale
    except Exception as e:
        print("Error getting system scaling:", str(e))
        return None, None

horizontal_scale, vertical_scale = get_system_scaling()
if horizontal_scale is not None and vertical_scale is not None:
    print("Horizontal system scaling:", horizontal_scale)
    print("Vertical system scaling:", vertical_scale)

pyScale = 100 / vertical_scale    

# Read screen resolution
info = pygame.display.Info()
width, height = info.current_w, info.current_h
print("Screen resolution width: ", width, "Screen resolution height: ",  height)

# Define background color
black = (0, 0, 0)

# Define window and starting point
window = pygame.display.set_mode((width, height), pygame.SCALED)
x_center, y_center = width // 2, height // 2

# Get the script directory
script_dir = os.path.dirname(__file__)

# Function to load images
def load(image_name):
    image = pygame.image.load(os.path.join(script_dir, image_name)).convert_alpha()
    return image

# Function to scale images
def load_and_scale(image_name, scale_factor=1.2):  # Default scale factor increased to 1.2
    print("__")
    sf = scale_factor
    image = load(image_name)
    image_width = image.get_width()
    image_height = image.get_height()
    scale_factor = height / image_height 
    scale_factor2 = width / image_width

    # Auto scaling
    if image_width > image_height:
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor2 * sf), int(image.get_height() * scale_factor2 * sf)))
        image_width2 = scaled_image.get_width()
        image_height2 = scaled_image.get_height()
        print("W>H", scale_factor2, image_width, image_width2, width, image_height, image_height2, height, image_name)
    elif image_width <= image_height:
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor * sf), int(image.get_height() * scale_factor * sf)))
        image_width2 = scaled_image.get_width()
        image_height2 = scaled_image.get_height()
        print("W<H", scale_factor, image_width, image_width2, width, image_height, image_height2, height, image_name)

    print("__")
    return scaled_image

# Load images
layer1 = load_and_scale("background.png")
layer2 = load_and_scale("hill.png", scale_factor=1.4)
layer3 = load_and_scale("tree.png", scale_factor=1.95)
layer4 = load_and_scale("fence.png", scale_factor=2)

# Initial positions (centered)
x_layer1, y_layer1 = x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2
x_layer2, y_layer2 = x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2
x_layer3, y_layer3 = x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2
x_layer4, y_layer4 = x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2

# Last known position
lastknown_x, lastknown_y = x_center, y_center

# Monitor distance to viewer in pixels
monitor_distance = 300.0

# Function to adjust layer positions
def anpassung_der_ebenen(kopf_x, kopf_y, basisposition, abstand_ebene, layer_width, layer_height, invert_x=False, invert_y=False):
    mittelpunkt_x, mittelpunkt_y = width // 2, height // 2

    # Calculate the displacement
    verschiebung_x = (mittelpunkt_x - kopf_x) * (abstand_ebene / monitor_distance)
    verschiebung_y = (mittelpunkt_y - kopf_y) * (abstand_ebene / monitor_distance)

    # Invert the x-axis movement if specified
    if invert_x:
        verschiebung_x = -verschiebung_x

    # Invert the y-axis movement if specified
    if invert_y:
        verschiebung_y = -verschiebung_y

    neue_position_x = basisposition[0] + verschiebung_x
    neue_position_y = basisposition[1] + verschiebung_y

    # Limit the movement to prevent showing the black background
    if neue_position_x > 0:
        neue_position_x = 0
    if neue_position_y > 0:
        neue_position_y = 0
    if neue_position_x < width - layer_width:
        neue_position_x = width - layer_width
    if neue_position_y < height - layer_height:
        neue_position_y = height - layer_height

    return neue_position_x, neue_position_y

# Game loop
running = True
try:
    while running:
        color_image, foreground_image = camera.get_frame()
        image = foreground_image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        face_center = face_detector.get_face_center(image)
        if face_center is not None:
            x_face_now, y_face_now = face_center
            lastknown_x = (x_face_now + lastknown_x * 9) / 10
            lastknown_y = (y_face_now + lastknown_y * 9) / 10
        else:
            lastknown_x = (lastknown_x * 9) / 10
            lastknown_y = (lastknown_y * 9) / 10

        print("x: ", x_face_now, "y: ", y_face_now)

        x_face_neu = ((x_face_now + lastknown_x * 9) / 10)
        y_face_neu = ((y_face_now + lastknown_y * 9) / 10)

        # Adjust the speed and inversion by changing the 'abstand_ebene' values and 'invert_x'/'invert_y' flags
        x_layer1, y_layer1 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2), 100, layer1.get_width(), layer1.get_height(), invert_x=True, invert_y=False)  # Slowest layer
        x_layer2, y_layer2 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2), 300, layer2.get_width(), layer2.get_height(), invert_x=True, invert_y=False)  # Faster layer
        x_layer4, y_layer4 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2), 900, layer4.get_width(), layer4.get_height(), invert_x=True, invert_y=False)  # Fastest layer
        x_layer3, y_layer3 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2), 700, layer3.get_width(), layer3.get_height(), invert_x=True, invert_y=False)   # Even faster layer
        

        window.fill(black)
        window.blit(layer1, (x_layer1, y_layer1))
        window.blit(layer2, (x_layer2, y_layer2)) 
        window.blit(layer3, (x_layer3, y_layer3))
        window.blit(layer4, (x_layer4, y_layer4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
finally:
    camera.stop()
    face_detector.close()
    pygame.quit()
    sys.exit()
