import pygame
import sys
import os
import cv2
import mediapipe as mp
import numpy as np
import ctypes
import time
from camera_manager import CameraManager
from face_detector import FaceCenterDetector
from utils import load_and_scale, get_system_scaling, load_and_scale_fullscreen
from layer_adjustment import anpassung_der_ebenen
from asset_manager import *

# Initialize Pygame
pygame.init()

# Initialize CameraManager
camera = CameraManager()
camera.start()

# Get system scaling factors
horizontal_scale, vertical_scale = get_system_scaling()

# Debug output of the scaling
if horizontal_scale is not None and vertical_scale is not None:
     print("Horizontal system scaling:", horizontal_scale)
     print("Vertical system scaling:", vertical_scale)

# Print screen dimensions for debugging
#print("Screen resolution width: ", width, "Screen resolution height: ",  height)

# Define a pygame window and starting point
window = pygame.display.set_mode((width, height), pygame.SCALED)
x_center, y_center = width // 2, height // 2

# Initialize scene variables
LevelSelected = True
wait = 0
current_time = 0

# Initialize layers
layer1 = layer2 = layer3 = layer4 = layer5 = layer6 = layer7 = None

def load_layers():
    global layer1, layer2, layer3, layer4, layer5, layer6, layer7
    layer1 = load_and_scale_fullscreen(image_layer1)
    layer2 = load_and_scale(image_layer2, scale_factor=scale_layer2)
    layer3 = load_and_scale(image_layer3, scale_factor=scale_layer3)
    layer4 = load_and_scale(image_layer4, scale_factor=scale_layer4)
    layer5 = load_and_scale(image_layer5, scale_factor=scale_layer5)
    layer6 = load_and_scale(image_layer6, scale_factor=scale_layer6)
    layer7 = load_and_scale(image_layer7, scale_factor=scale_layer7)

# Initial layer loading
load_layers()

# Load frame and curtains
layer0_frame = load_and_scale_fullscreen(image_layer0_frame)
layer0_leftCurtain = load_and_scale_fullscreen(image_layer0_left_curtain)
layer0_rightCurtain = load_and_scale_fullscreen(image_layer0_right_curtain)

# Initialize positions
x_layer1, y_layer1 = x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2
x_layer2, y_layer2 = x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2
x_layer3, y_layer3 = x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2
x_layer4, y_layer4 = x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2
x_layer5, y_layer5 = x_center - layer5.get_width() // 2, y_center - layer5.get_height() // 2
x_layer6, y_layer6 = x_center - layer6.get_width() // 2, y_center - layer6.get_height() // 2
x_layer7, y_layer7 = x_center - layer7.get_width() // 2, y_center - layer7.get_height() // 2

# Last known position 
lastknown_x, lastknown_y = x_center, y_center

# Initialize face position
x_face_now, y_face_now = x_center, y_center

# Initialize game loop variables
running = True
face_detector = FaceCenterDetector()
curtains_visible = True
CurtainsClosed = False

# Curtain animation variables
curtain_speed = 10
left_curtain_x = 0
right_curtain_x = width - layer0_rightCurtain.get_width()
target_left_curtain_x = 0
target_right_curtain_x = width - layer0_rightCurtain.get_width()

# Curtain close counter variables
curtain_close_counter = 0
last_curtain_state = curtains_visible

def switch_scene():
    global LevelSelected, CurtainsClosed, image_layer1, image_layer2, image_layer3, image_layer4, image_layer5, image_layer6, image_layer7
    global speed_layer1, speed_layer2, speed_layer3, speed_layer4, speed_layer5, speed_layer6, speed_layer7
    global scale_layer1, scale_layer2, scale_layer3, scale_layer4, scale_layer5, scale_layer6, scale_layer7

    #print("Inside switch_scene function")  # Debug print

    if CurtainsClosed:
        if LevelSelected:
            print("City -> Garden")
            # Garden Scene
            image_layer1 = "HimmelF.png"
            image_layer2 = "HintergrundF.png"
            image_layer3 = "HausF.png"
            image_layer4 = "TerasseFTerasse.png"
            image_layer5 = "VordergrundF.png"
            image_layer6 = "PflanzenVorneF.png"
            image_layer7 = "Bee.png"

            speed_layer1 = 800
            speed_layer2 = 700
            speed_layer3 = 560
            speed_layer4 = 480
            speed_layer5 = 380
            speed_layer6 = 300

            scale_layer1 = 1.2
            scale_layer2 = 1.25
            scale_layer3 = 1.2
            scale_layer4 = 1.2
            scale_layer5 = 1.2
            scale_layer6 = 1.2

            LevelSelected = False
        else:
            print("Garden -> City")
            # City Scene
            image_layer1 = "CitySky.png"
            image_layer2 = "CitySky.png"
            image_layer3 = "CitySky.png"
            image_layer4 = "CityBackground.png"
            image_layer5 = "CityMidground.png"
            image_layer6 = "CityForeground.png"
            image_layer7 = "hot-air-balloon.png"

            speed_layer1 = 0
            speed_layer2 = 0
            speed_layer3 = 0
            speed_layer4 = 260
            speed_layer5 = 180
            speed_layer6 = 100

            scale_layer1 = 1
            scale_layer2 = 1
            scale_layer3 = 1
            scale_layer4 = 1.45
            scale_layer5 = 1.3
            scale_layer6 = 1.1

            LevelSelected = True

        # Reload Images
        load_layers()
        #print("Layers reloaded")  # Debug print
        
        # Reset CurtainsClosed flag after switching
        CurtainsClosed = False

# Game loop
with mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while running:
        current_time = time.time()

        # Get a new frame from the camera
        color_image_rgb, foreground_image = camera.get_frame()
        if color_image_rgb is None or foreground_image is None:
            continue
        image = foreground_image

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if current_time - wait >= 1:
                        curtains_visible = True
                        wait = current_time

        # Process the gathered frame for face detection
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)
        
        # Try to detect a face and retrieve the coordinates of the center of the face
        face_center = face_detector.get_face_center(image)
        if face_center is not None:
            x_face_now, y_face_now = face_center 
            x_face_now = x_face_now * width
            y_face_now = y_face_now * height

            lastknown_x, lastknown_y = x_face_now, y_face_now

            # Call check_upper_right_quadrant function
            face_detector.check_upper_right_quadrant(x_face_now, y_face_now, width, height)
        elif lastknown_x is not None and lastknown_y is not None:
            x_face_now, y_face_now = lastknown_x, lastknown_y
        else:
            x_face_now, y_face_now = x_center, y_center
        
        # Smooth the face movement
        y_face_neu = ((y_face_now*3 + lastknown_y * 9) / 12)
        x_face_neu = ((x_face_now*3 + lastknown_x * 9) / 12)
        #print(x_face_neu, y_face_neu)

        # Process the frame to detect if a face is present to control the curtains
        face_detector.process_frame(image)
        curtains_visible = not face_detector.face_detected

        # Check if curtains have just closed
        if curtains_visible and not last_curtain_state:
            curtain_close_counter += 1
            if curtain_close_counter > 1:
                curtain_close_counter = 0
            #print(f"Curtains closed. Counter: {curtain_close_counter}")

        last_curtain_state = curtains_visible

        # Update target positions for curtains

        #print(f"Curtains visible: {curtains_visible}")  # Debug print
        if curtains_visible:
            target_left_curtain_x = 0
            target_right_curtain_x = width - layer0_rightCurtain.get_width()
            #print(f"Left curtain: {left_curtain_x}/{target_left_curtain_x}, Right curtain: {right_curtain_x}/{target_right_curtain_x}")  # Debug print
            if left_curtain_x == target_left_curtain_x and right_curtain_x == target_right_curtain_x:
                #print("Curtains fully closed")  # Debug print
                if not CurtainsClosed:
                    #print("Attempting to switch scene")  # Debug print
                    CurtainsClosed = True
                    switch_scene()
        else:
            target_left_curtain_x = -layer0_leftCurtain.get_width()
            target_right_curtain_x = width
            if CurtainsClosed:
                #print("Curtains opening, resetting CurtainsClosed")  # Debug print
                CurtainsClosed = False

        # Move curtains towards target positions
        if left_curtain_x < target_left_curtain_x:
            left_curtain_x = min(left_curtain_x + curtain_speed, target_left_curtain_x)
        elif left_curtain_x > target_left_curtain_x:
            left_curtain_x = max(left_curtain_x - curtain_speed, target_left_curtain_x)

        if right_curtain_x < target_right_curtain_x:
            right_curtain_x = min(right_curtain_x + curtain_speed, target_right_curtain_x)
        elif right_curtain_x > target_right_curtain_x:
            right_curtain_x = max(right_curtain_x - curtain_speed, target_right_curtain_x)

        #print(f"CurtainsClosed: {CurtainsClosed}")  # Debug print

        # Check if the curtains are fully closed
        # if curtains_visible:
        #     if left_curtain_x == 0 and right_curtain_x == width - layer0_rightCurtain.get_width():
        #         CurtainsClosed = True
        #     else:
        #         CurtainsClosed = False
        # else:
        #     CurtainsClosed = False

        # Debug output for CurtainsClosed
        #print("CurtainsClosed:", CurtainsClosed)

        # Adjust the layer positions based on the face position
        x_layer1, y_layer1 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer1.get_width() // 2, y_center - layer1.get_height() // 2), speed_layer1, layer1.get_width(), layer1.get_height())
        x_layer2, y_layer2 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer2.get_width() // 2, y_center - layer2.get_height() // 2), speed_layer2, layer2.get_width(), layer2.get_height())
        x_layer3, y_layer3 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer3.get_width() // 2, y_center - layer3.get_height() // 2), speed_layer3, layer3.get_width(), layer3.get_height())
        x_layer4, y_layer4 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer4.get_width() // 2, y_center - layer4.get_height() // 2), speed_layer4, layer4.get_width(), layer4.get_height())
        x_layer5, y_layer5 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer5.get_width() // 2, y_center - layer5.get_height() // 2), speed_layer5, layer5.get_width(), layer5.get_height())
        x_layer6, y_layer6 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer6.get_width() // 2, y_center - layer6.get_height() // 2), speed_layer6, layer6.get_width(), layer6.get_height())
        x_layer7, y_layer7 = anpassung_der_ebenen(x_face_neu, y_face_neu, (x_center - layer7.get_width() // 2, y_center - layer7.get_height() // 2), speed_layer7, layer7.get_width(), layer7.get_height(), layer_name="hot-air-ballon.png")

        # Create a black background
        window.fill(BLACK)

        # Draw the layers
        window.blit(layer1, (x_layer1, y_layer1))
        window.blit(layer2, (x_layer2, y_layer2)) 
        window.blit(layer3, (x_layer3, y_layer3))
        window.blit(layer4, (x_layer4, y_layer4))
        window.blit(layer5, (x_layer5, y_layer5))
        window.blit(layer7, (x_layer7, y_layer7))
        window.blit(layer6, (x_layer6, y_layer6))
        window.blit(layer0_frame, (0, 0))

        # Draw a small cross at the face coordinates if activated in asset manager
        if draw_face_position_crosshair == True:
            cross_color = (255, 0, 0)  # Red color
            cross_size = 10  # Size of the cross
            x_crosshair = width - x_face_neu
            pygame.draw.line(window, cross_color, (x_crosshair - cross_size, y_face_neu), (x_crosshair + cross_size, y_face_neu), 2)
            pygame.draw.line(window, cross_color, (x_crosshair, y_face_neu - cross_size), (x_crosshair, y_face_neu + cross_size), 2)

        # Draw the curtains at their current positions
        window.blit(layer0_leftCurtain, (left_curtain_x, 0))
        window.blit(layer0_rightCurtain, (right_curtain_x, 0))

        # Update the display
        pygame.display.flip()

# Clean up resources
camera.stop()
face_detector.close()
pygame.quit()
sys.exit()