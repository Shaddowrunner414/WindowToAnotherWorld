import cv2
import pygame
import sys
import os
import mediapipe as mp
import ctypes

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame and OpenCV
pygame.init()
cap = cv2.VideoCapture(0)  # 0 stands for the first camera

# Load face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while running:
        success, image = cap.read()
        if not success:
            print("Could not start the webcam")
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        x_face_now, y_face_now = x_center, y_center

        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x_face_now = int(bbox.xmin * width)
                y_face_now = int(bbox.ymin * height)
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

         # Draw a small cross at the face coordinates
        cross_color = (255, 0, 0)  # Red color
        cross_size = 10  # Size of the cross
        pygame.draw.line(window, cross_color, (x_face_neu - cross_size, y_face_neu), (x_face_neu + cross_size, y_face_neu), 2)
        pygame.draw.line(window, cross_color, (x_face_neu, y_face_neu - cross_size), (x_face_neu, y_face_neu + cross_size), 2)
q

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

cap.release()
pygame.quit()
sys.exit()

